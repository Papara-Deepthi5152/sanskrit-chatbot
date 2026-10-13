/**
 * Vāgdevī - Sanskrit AI Chatbot Client-Side Application
 * Handles chat messaging, speech synthesis (TTS), speech recognition (STT),
 * transliteration helper, grammar table rendering, sandhi solver, and quizzes.
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatInput = document.getElementById('chat-input');
    const btnSend = document.getElementById('btn-send-message');
    const messagesList = document.getElementById('messages-list');
    const btnVoice = document.getElementById('btn-voice-input');
    const btnToggleKeyboard = document.getElementById('btn-toggle-keyboard');
    const devanagariToolbar = document.getElementById('devanagari-toolbar');
    const translitPreviewBar = document.getElementById('translit-preview-bar');
    const translitPreviewText = document.getElementById('translit-preview-text');
    const btnUsePreview = document.getElementById('btn-use-preview');
    const btnClearChat = document.getElementById('btn-clear-chat');
    const voiceSelect = document.getElementById('voice-select');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const navItems = document.querySelectorAll('.nav-item');
    const tabPanes = document.querySelectorAll('.tab-pane');

    // Sidebar Shloka elements
    const sidebarSodText = document.getElementById('sidebar-sod-text');
    const btnRefreshSod = document.getElementById('btn-refresh-sod');

    // Grammar elements
    const grammarArea = document.getElementById('grammar-display-area');
    const grammarChips = document.querySelectorAll('.btn-gram-chip');

    // Sandhi elements
    const sandhiW1 = document.getElementById('sandhi-w1');
    const sandhiW2 = document.getElementById('sandhi-w2');
    const btnSandhiSolve = document.getElementById('btn-sandhi-solve');
    const sandhiLiveResult = document.getElementById('sandhi-live-result');
    const sandhiRulesGrid = document.getElementById('sandhi-rules-grid');

    // Wisdom & Quiz elements
    const shlokasGrid = document.getElementById('shlokas-collection-grid');
    const arenaContainer = document.getElementById('arena-question-container');
    const arenaScoreDisplay = document.getElementById('arena-score-display');
    const btnArenaNext = document.getElementById('btn-arena-next');

    let speechSynth = window.speechSynthesis;
    let availableVoices = [];
    let isRecognizing = false;
    let recognition = null;
    let translitDebounceTimer = null;
    let currentArenaQuestion = null;

    // ------------------------------------------------------------------------
    // Tab Navigation
    // ------------------------------------------------------------------------
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const tabId = item.getAttribute('data-tab');
            navItems.forEach(n => n.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            item.classList.add('active');
            const targetPane = document.getElementById(tabId);
            if (targetPane) targetPane.classList.add('active');

            // Close sidebar on mobile after tab click
            if (window.innerWidth <= 900) {
                sidebar.classList.remove('open');
            }

            // Lazy load tab data
            if (tabId === 'grammar-view' && !grammarArea.hasChildNodes()) {
                loadGrammarItem('shabda', 'rama');
            } else if (tabId === 'sandhi-view' && !sandhiRulesGrid.hasChildNodes()) {
                loadSandhiRules();
            } else if (tabId === 'shloka-view' && !shlokasGrid.hasChildNodes()) {
                loadShlokasLibrary();
            } else if (tabId === 'quiz-view' && !currentArenaQuestion) {
                loadArenaQuestion();
            }
        });
    });

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    // ------------------------------------------------------------------------
    // Speech Synthesis (TTS) Setup
    // ------------------------------------------------------------------------
    function populateVoices() {
        if (!speechSynth) return;
        availableVoices = speechSynth.getVoices();
        voiceSelect.innerHTML = '';

        // Find Hindi or Indian English voice preferred for Sanskrit
        let preferredIndex = 0;
        availableVoices.forEach((voice, i) => {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = `${voice.name} (${voice.lang})`;

            if (voice.lang.includes('hi') || voice.lang.includes('sa') || voice.lang === 'hi-IN') {
                preferredIndex = i;
            } else if (voice.lang === 'en-IN' && preferredIndex === 0) {
                preferredIndex = i;
            }

            voiceSelect.appendChild(option);
        });

        if (availableVoices.length > 0) {
            voiceSelect.selectedIndex = preferredIndex;
        }
    }

    if (speechSynth) {
        populateVoices();
        if (speechSynth.onvoiceschanged !== undefined) {
            speechSynth.onvoiceschanged = populateVoices;
        }
    }

    window.speakSanskrit = function(text) {
        if (!speechSynth) return;
        speechSynth.cancel(); // Stop current speech
        const cleanText = text.replace(/[\*\#\_\|\[\]\(\)\n]/g, ' ').trim();
        const utter = new SpeechSynthesisUtterance(cleanText);

        const selIndex = voiceSelect.value;
        if (availableVoices[selIndex]) {
            utter.voice = availableVoices[selIndex];
        }

        utter.rate = 0.88; // Slower, solemn educational pace
        utter.pitch = 1.0;
        speechSynth.speak(utter);
    };

    // ------------------------------------------------------------------------
    // Speech Recognition (STT) Setup
    // ------------------------------------------------------------------------
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'hi-IN'; // Works very well with Devanagari phonetics

        recognition.onstart = () => {
            isRecognizing = true;
            btnVoice.classList.add('recording');
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            chatInput.value = transcript;
            btnVoice.classList.remove('recording');
            isRecognizing = false;
            sendMessage();
        };

        recognition.onerror = () => {
            btnVoice.classList.remove('recording');
            isRecognizing = false;
        };

        recognition.onend = () => {
            btnVoice.classList.remove('recording');
            isRecognizing = false;
        };

        btnVoice.addEventListener('click', () => {
            if (isRecognizing) {
                recognition.stop();
            } else {
                recognition.start();
            }
        });
    } else {
        btnVoice.style.display = 'none';
    }

    // ------------------------------------------------------------------------
    // Chat Messaging
    // ------------------------------------------------------------------------
    async function sendMessage(customText = null) {
        const text = customText !== null ? customText : chatInput.value.trim();
        if (!text) return;

        // Clear input and previews
        chatInput.value = '';
        translitPreviewBar.classList.add('hidden');

        // Append User Bubble
        appendUserMessage(text);

        // Show typing indicator
        const typingId = appendTypingIndicator();

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });

            removeElement(typingId);

            if (!res.ok) throw new Error('Network error');
            const data = await res.json();
            appendBotMessage(data);

        } catch (err) {
            removeElement(typingId);
            appendBotMessage({
                text_sa: "क्षम्यताम्! त्रुटिः संजाता।",
                text_iast: "Kṣamyatām! Truṭiḥ sañjātā.",
                text_en: "Sorry, a communication error occurred. Please try again.",
                follow_ups: ["नमस्ते", "Try again"]
            });
        }
    }

    function appendUserMessage(text) {
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble user-message';
        bubble.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-user"></i></div>
            <div class="message-body">
                <div class="msg-header">
                    <span class="sender-name">भवान् (You)</span>
                </div>
                <div class="sa-text">${escapeHtml(text)}</div>
            </div>
        `;
        messagesList.appendChild(bubble);
        scrollToBottom();
    }

    function appendBotMessage(data) {
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble bot-message';

        const saText = data.text_sa || '';
        const iastText = data.text_iast || '';
        const enText = (data.text_en || '').replace(/\n/g, '<br>');
        const htmlContent = data.html_content || '';
        const followUps = data.follow_ups || [];
        const audioText = data.audio_text || saText;

        const chipsHtml = followUps.map(chip =>
            `<button class="chip" data-query="${escapeHtml(chip)}">${escapeHtml(chip)}</button>`
        ).join('');

        bubble.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-feather-pointed"></i></div>
            <div class="message-body">
                <div class="msg-header">
                    <span class="sender-name">वाग्देवी (Vāgdevī)</span>
                    <div class="msg-tools">
                        <button class="btn-tool btn-speak" title="Pronounce Sanskrit"><i class="fa-solid fa-volume-high"></i></button>
                        <button class="btn-tool btn-copy" title="Copy Sanskrit text"><i class="fa-regular fa-copy"></i></button>
                    </div>
                </div>
                <div class="sa-text">${escapeHtml(saText).replace(/\n/g, '<br>')}</div>
                ${iastText ? `<div class="iast-text">${escapeHtml(iastText).replace(/\n/g, '<br>')}</div>` : ''}
                <div class="en-text">${enText}</div>
                ${htmlContent ? `<div class="card-wrapper">${htmlContent}</div>` : ''}
                ${chipsHtml ? `<div class="prompt-chips">${chipsHtml}</div>` : ''}
            </div>
        `;

        // Attach event listeners
        bubble.querySelector('.btn-speak').addEventListener('click', () => {
            speakSanskrit(audioText);
        });

        bubble.querySelector('.btn-copy').addEventListener('click', () => {
            navigator.clipboard.writeText(saText);
            const copyBtn = bubble.querySelector('.btn-copy');
            copyBtn.innerHTML = '<i class="fa-solid fa-check"></i>';
            setTimeout(() => { copyBtn.innerHTML = '<i class="fa-regular fa-copy"></i>'; }, 2000);
        });

        bubble.querySelectorAll('.chip').forEach(btn => {
            btn.addEventListener('click', () => {
                const query = btn.getAttribute('data-query');
                sendMessage(query);
            });
        });

        messagesList.appendChild(bubble);
        scrollToBottom();
    }

    function appendTypingIndicator() {
        const id = 'typing-' + Date.now();
        const bubble = document.createElement('div');
        bubble.id = id;
        bubble.className = 'message-bubble bot-message typing-indicator';
        bubble.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-feather-pointed"></i></div>
            <div class="message-body" style="padding: 12px 18px;">
                <span style="font-size: 13px; color: var(--text-secondary);"><i class="fa-solid fa-spinner fa-spin"></i> वाग्देवी चिन्तयति... (Vāgdevī is pondering...)</span>
            </div>
        `;
        messagesList.appendChild(bubble);
        scrollToBottom();
        return id;
    }

    function removeElement(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        messagesList.scrollTop = messagesList.scrollHeight;
    }

    function escapeHtml(str) {
        return str.replace(/&/g, '&amp;')
                  .replace(/</g, '&lt;')
                  .replace(/>/g, '&gt;')
                  .replace(/"/g, '&quot;')
                  .replace(/'/g, '&#039;');
    }

    // Send on button click or Enter key
    btnSend.addEventListener('click', () => sendMessage());
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });

    // Delegate chips inside existing chat
    messagesList.addEventListener('click', (e) => {
        const chip = e.target.closest('.chip');
        if (chip) {
            const query = chip.getAttribute('data-query');
            sendMessage(query);
        }
    });

    // Global quiz answer button handler
    window.sendQuizAnswer = function(choiceNumber) {
        sendMessage(String(choiceNumber));
    };

    // Clear chat
    btnClearChat.addEventListener('click', () => {
        if (confirm('वार्तालापं स्वच्छीकर्तुम् इच्छति किम्? (Clear chat history?)')) {
            messagesList.innerHTML = '';
            sendMessage('namaste');
        }
    });

    // ------------------------------------------------------------------------
    // Devanagari Virtual Toolbar
    // ------------------------------------------------------------------------
    btnToggleKeyboard.addEventListener('click', () => {
        devanagariToolbar.classList.toggle('hidden');
    });

    devanagariToolbar.addEventListener('click', (e) => {
        const tbBtn = e.target.closest('.tb-btn');
        if (tbBtn) {
            const insertText = tbBtn.getAttribute('data-insert');
            insertAtCursor(chatInput, insertText);
            chatInput.focus();
        }
    });

    function insertAtCursor(input, text) {
        const start = input.selectionStart || input.value.length;
        const end = input.selectionEnd || input.value.length;
        input.value = input.value.substring(0, start) + text + input.value.substring(end);
        input.selectionStart = input.selectionEnd = start + text.length;
    }

    // ------------------------------------------------------------------------
    // Live Transliteration Preview Hint
    // ------------------------------------------------------------------------
    chatInput.addEventListener('input', () => {
        const val = chatInput.value.trim();
        clearTimeout(translitDebounceTimer);

        // If Latin text entered with length >= 3 and no Devanagari
        const hasLatin = /[a-zA-Z]/.test(val);
        const hasDeva = /[\u0900-\u097F]/.test(val);

        if (hasLatin && !hasDeva && val.length >= 2) {
            translitDebounceTimer = setTimeout(async () => {
                try {
                    const res = await fetch('/api/transliterate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ text: val })
                    });
                    const d = await res.json();
                    if (d.devanagari && d.devanagari !== val) {
                        translitPreviewText.textContent = d.devanagari;
                        translitPreviewBar.classList.remove('hidden');
                    } else {
                        translitPreviewBar.classList.add('hidden');
                    }
                } catch (e) {
                    translitPreviewBar.classList.add('hidden');
                }
            }, 250);
        } else {
            translitPreviewBar.classList.add('hidden');
        }
    });

    btnUsePreview.addEventListener('click', () => {
        chatInput.value = translitPreviewText.textContent;
        translitPreviewBar.classList.add('hidden');
        chatInput.focus();
    });

    // ------------------------------------------------------------------------
    // Shloka of the Day
    // ------------------------------------------------------------------------
    async function refreshShlokaOfDay() {
        try {
            const res = await fetch('/api/shloka-of-the-day');
            const data = await res.json();
            sidebarSodText.textContent = data.shloka_sa.split('\n')[0] + '...';
        } catch (e) {}
    }

    btnRefreshSod.addEventListener('click', refreshShlokaOfDay);
    refreshShlokaOfDay();

    // ------------------------------------------------------------------------
    // Grammar Hub Controller
    // ------------------------------------------------------------------------
    grammarChips.forEach(chip => {
        chip.addEventListener('click', () => {
            grammarChips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            const type = chip.getAttribute('data-type');
            const name = chip.getAttribute('data-name');
            loadGrammarItem(type, name);
        });
    });

    async function loadGrammarItem(type, name) {
        grammarArea.innerHTML = '<p class="loading-text">अध्ययनं प्रचलति... (Loading grammar table...)</p>';
        try {
            const url = type === 'shabda' ? `/api/grammar/shabda/${name}` : `/api/grammar/dhatu/${name}`;
            const res = await fetch(url);
            const data = await res.json();

            if (type === 'shabda') {
                renderShabdaTable(data);
            } else {
                renderDhatuTable(data);
            }
        } catch (e) {
            grammarArea.innerHTML = '<p class="error-text">विवरणं न लब्धम् (Could not load table).</p>';
        }
    }

    function renderShabdaTable(data) {
        const rows = data.table.map(r => `
            <tr>
                <td><strong>${r.vibhakti}</strong></td>
                <td><span class="sa-cell">${r.singular}</span></td>
                <td><span class="sa-cell">${r.dual}</span></td>
                <td><span class="sa-cell">${r.plural}</span></td>
                <td>${r.usage}</td>
            </tr>
        `).join('');

        grammarArea.innerHTML = `
            <div class="card">
                <h3>शब्दरूपम्: ${data.word} (${data.transliteration})</h3>
                <p class="subtitle" style="color: var(--text-secondary); margin-bottom: 12px;">
                    ${data.type} &bull; ${data.meaning}
                </p>
                <div class="table-wrapper">
                    <table class="sanskrit-table">
                        <thead>
                            <tr><th>विभक्तिः (Case)</th><th>एकवचनम् (Singular)</th><th>द्विवचनम् (Dual)</th><th>बहुवचनम् (Plural)</th><th>Usage</th></tr>
                        </thead>
                        <tbody>${rows}</tbody>
                    </table>
                </div>
            </div>
        `;
    }

    function renderDhatuTable(data) {
        let lakarasHtml = '';
        for (const [k, lk] of Object.entries(data.lakaras)) {
            const rows = lk.forms.map(r => `
                <tr>
                    <td><strong>${r.purusha}</strong></td>
                    <td><span class="sa-cell">${r.singular}</span></td>
                    <td><span class="sa-cell">${r.dual}</span></td>
                    <td><span class="sa-cell">${r.plural}</span></td>
                    <td>${r.meaning}</td>
                </tr>
            `).join('');

            lakarasHtml += `
                <div style="margin-top: 20px;">
                    <h4 style="color: #923805; margin-bottom: 8px;">${lk.name}</h4>
                    <div class="table-wrapper">
                        <table class="sanskrit-table">
                            <thead>
                                <tr><th>पुरुषः</th><th>एकवचनम्</th><th>द्विवचनम्</th><th>बहुवचनम्</th><th>English Meaning</th></tr>
                            </thead>
                            <tbody>${rows}</tbody>
                        </table>
                    </div>
                </div>
            `;
        }

        grammarArea.innerHTML = `
            <div class="card">
                <h3>धातुरूपम्: ${data.dhatu} (${data.transliteration})</h3>
                <p class="subtitle" style="color: var(--text-secondary);">
                    <strong>अर्थः:</strong> ${data.meaning} &bull; <strong>गणः:</strong> ${data.gana}
                </p>
                ${lakarasHtml}
            </div>
        `;
    }

    // ------------------------------------------------------------------------
    // Sandhi Studio Controller
    // ------------------------------------------------------------------------
    async function loadSandhiRules() {
        try {
            const res = await fetch('/api/rules/sandhi');
            const rules = await res.json();
            sandhiRulesGrid.innerHTML = rules.map(r => `
                <div class="sandhi-card">
                    <h3>${r.name}</h3>
                    <div class="sutra-badge">सूत्रम्: ${r.sutra}</div>
                    <p style="font-size: 13px; color: var(--text-secondary); margin-bottom: 10px;">${r.rule}</p>
                    <ul style="font-size: 13px; padding-left: 18px;">
                        ${r.examples.map(ex => `<li><code>${ex.split}</code> &rarr; <strong>${ex.joined}</strong></li>`).join('')}
                    </ul>
                </div>
            `).join('');
        } catch (e) {}
    }

    btnSandhiSolve.addEventListener('click', async () => {
        const w1 = sandhiW1.value.trim();
        const w2 = sandhiW2.value.trim();
        if (!w1 || !w2) return;

        sandhiLiveResult.innerHTML = '<p class="loading-text">सन्धिः क्रियते... (Joining...)</p>';
        try {
            const res = await fetch('/api/sandhi', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ word1: w1, word2: w2 })
            });
            const data = await res.json();

            sandhiLiveResult.innerHTML = `
                <div class="sandhi-result">
                    <div class="sandhi-formula">
                        <strong>${escapeHtml(w1)}</strong> + <strong>${escapeHtml(w2)}</strong> = 
                        <span class="highlight-result">${data.joined}</span> (${data.joined_iast})
                    </div>
                    <div class="sandhi-rule">
                        <strong>नियमः:</strong> ${data.rule_name} &bull; <em>${data.sutra}</em>
                    </div>
                    <p style="font-size: 13px; color: var(--text-primary); margin-top: 6px;">${data.explanation}</p>
                </div>
            `;
        } catch (e) {
            sandhiLiveResult.innerHTML = '<p class="error-text">Error joining words.</p>';
        }
    });

    // ------------------------------------------------------------------------
    // Wisdom (Shlokas) Library Controller
    // ------------------------------------------------------------------------
    async function loadShlokasLibrary() {
        try {
            // We can fetch from chat dialogue manager knowledge base via api or preset
            const res = await fetch('/api/shloka-of-the-day');
            // Fetch multiple shlokas
            const promises = [1, 2, 3, 4, 5].map(() => fetch('/api/shloka-of-the-day').then(r => r.json()));
            const list = await Promise.all(promises);

            // Deduplicate by id
            const unique = [];
            const seen = new Set();
            for (const item of list) {
                if (!seen.has(item.id)) {
                    seen.add(item.id);
                    unique.push(item);
                }
            }

            shlokasGrid.innerHTML = unique.map(s => `
                <div class="shloka-card">
                    <div class="shloka-source">📜 ${s.source}</div>
                    <div class="shloka-sanskrit">${s.shloka_sa.replace(/\n/g, '<br>')}</div>
                    <div class="shloka-iast">${s.shloka_iast.replace(/\n/g, '<br>')}</div>
                    <div class="shloka-breakdown">
                        <p><strong>पदच्छेदः:</strong> ${s.padachheda}</p>
                        <p><strong>अन्वयः:</strong> ${s.anvaya}</p>
                    </div>
                    <div class="shloka-meaning">
                        <p><strong>Meaning:</strong> ${s.meaning_en}</p>
                        <p style="margin-top: 6px;"><strong>💡 Lesson:</strong> <em>${s.lesson}</em></p>
                    </div>
                    <div style="margin-top: 14px;">
                        <button class="btn-secondary" onclick="speakSanskrit('${escapeHtml(s.shloka_sa.replace(/\n/g, ' '))}')">
                            <i class="fa-solid fa-volume-high"></i> Recite (पठतु)
                        </button>
                    </div>
                </div>
            `).join('');
        } catch (e) {}
    }

    // ------------------------------------------------------------------------
    // Quiz Arena Controller
    // ------------------------------------------------------------------------
    async function loadArenaQuestion() {
        arenaContainer.innerHTML = '<p class="loading-text">प्रश्नः आगच्छति... (Loading question...)</p>';
        try {
            const res = await fetch('/api/quiz/question');
            currentArenaQuestion = await res.json();

            const optionsHtml = currentArenaQuestion.options.map((opt, idx) => `
                <button class="btn-quiz-option" onclick="submitArenaAnswer(${idx})">
                    <span class="opt-num">${idx + 1}</span> ${escapeHtml(opt)}
                </button>
            `).join('');

            arenaContainer.innerHTML = `
                <div class="quiz-box">
                    <div class="quiz-category">🏷️ ${currentArenaQuestion.category}</div>
                    <div class="quiz-question-sa">${currentArenaQuestion.question_sa}</div>
                    <div class="quiz-question-en">${currentArenaQuestion.question_en}</div>
                    <div class="quiz-options">${optionsHtml}</div>
                </div>
            `;
        } catch (e) {
            arenaContainer.innerHTML = '<p class="error-text">Could not load quiz question.</p>';
        }
    }

    window.submitArenaAnswer = async function(idx) {
        if (!currentArenaQuestion) return;
        try {
            const res = await fetch('/api/quiz/answer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    qid: currentArenaQuestion.id,
                    answer_idx: idx
                })
            });
            const data = await res.json();

            arenaScoreDisplay.textContent = `${data.score.correct} / ${data.score.total}`;

            const resultHtml = `
                <div class="quiz-result-box ${data.is_correct ? 'success' : 'notice'}">
                    <h4>${data.is_correct ? '🎉 साधु! समीचीनम् उत्तरम्!' : '💡 प्रयत्नः उत्तमः!'}</h4>
                    <p><strong>Correct Answer:</strong> ${data.correct_answer}</p>
                    <p><strong>विवरणम्:</strong> ${data.explanation}</p>
                </div>
            `;

            arenaContainer.insertAdjacentHTML('beforeend', resultHtml);

            // Disable buttons after answer
            arenaContainer.querySelectorAll('.btn-quiz-option').forEach(b => b.disabled = true);

        } catch (e) {}
    };

    btnArenaNext.addEventListener('click', loadArenaQuestion);
});
