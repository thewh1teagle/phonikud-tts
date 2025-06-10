function hasDiacritics(text) {
    // Check for Hebrew diacritics (nikud) in the range \u05b0 to \u05c7
    return /[\u05b0-\u05c7]/.test(text);
}

function generate(mode) {
    const statusId = mode + "-status";
    const buttonId = mode + "-btn";
    const statusElement = document.getElementById(statusId);
    const buttonElement = document.getElementById(buttonId);
    const alertElement = document.getElementById("diacritics-alert");

    // Hide alert first
    if (alertElement) {
        alertElement.style.display = "none";
    }

    // Check for diacritics if in diacritics mode
    if (mode === "diacritics") {
        const text = document.getElementById("diacritics-input").value;
        if (text && !hasDiacritics(text)) {
            alertElement.style.display = "block";
            statusElement.style.display = 'none'
            return;
        }
    }

    // Show and update status
    statusElement.style.display = "flex";
    statusElement.textContent = "Generating audio...";
    statusElement.className = "status-indicator status-generating";

    // Disable button
    buttonElement.disabled = true;

    // Hide audio section
    const audioSection = document.getElementById("audio-section");
    const audio = document.getElementById("audio");
    audio.pause();
    audio.src = "";

    const formData = new FormData();
    formData.append("mode", mode);
    formData.append(
        "text",
        mode === "phonemes" ? "" : document.getElementById(mode + "-input").value
    );
    formData.append("phonemes", document.getElementById("phonemes-input").value);

    fetch("/generate", { method: "POST", body: formData })
        .then((res) => res.json())
        .then((data) => {
            // Update all fields with returned data
            if (data.diacritics) {
                document.getElementById("diacritics-input").value = data.diacritics || "";
            }
            if (data.phonemes) {
                document.getElementById("phonemes-input").value = data.phonemes || "";
            }
            
            

            // Set up audio
            audio.src = data.audio;
            audioSection.style.display = "block";

            // Auto-play audio
            setTimeout(() => {
                audio.play().catch(e => console.log("Auto-play prevented by browser"));
            }, 300);

            // Update status to success
            statusElement.textContent = "✓ Audio generated successfully";
            statusElement.className = "status-indicator status-ready";
        })
        .catch((err) => {
            statusElement.textContent = "✗ Error generating audio";
            statusElement.className = "status-indicator status-error";
            console.error(err);
        })
        .finally(() => {
            // Re-enable button
            buttonElement.disabled = false;
        });
}

const diacriticsInput = document.getElementById('diacritics-input');
const phonemesInput = document.getElementById('phonemes-input');
const textInput = document.getElementById('text-input');
const btnHatama = document.getElementById('btnHatama');
const btnVocalShva = document.getElementById('btnVocalShva');
const btnStress = document.getElementById('btnStress');

function insertAtCursor(charToInsert, inputName) {
    const inputElement = inputName == 'diacritics' ? diacriticsInput : inputName == 'text' ? textInput : phonemesInput
    const start = inputElement.selectionStart;
    const end = inputElement.selectionEnd;
    const text = inputElement.value;

    inputElement.value = text.slice(0, start) + charToInsert + text.slice(end);
    // Move cursor after inserted char
    inputElement.selectionStart = inputElement.selectionEnd = start + charToInsert.length;
    inputElement.focus();
}

btnHatama.addEventListener('click', () => {
    insertAtCursor('\u05ab'); // Hebrew Shin Dot (Hatama)
});

btnVocalShva.addEventListener('click', () => {
    insertAtCursor('\u05bd'); // Hebrew Vocal Shva
});

// btnStress.addEventListener('click', () => {
//     insertAtCursor('\u05bd');
// })

// Set initial example text
window.addEventListener('load', () => {
    setTimeout(() => {
        document.getElementById("text-input").value =
            "מה שבהגדרה משאיר את הכלכלה ההונגרית מאחור, אפילו ביחס למדינות כמו פולין.";
        document.getElementById('diacritics-input').value = "מָה שֶׁבַּ|הַגְדָּרָה מַשְׁאִיר אֶת הַ|כַּלְכָּלָה הַ|הוּנְגָּרִית מֵאָחוֹר, אֲפִ֫ילּוּ בְּֽ|יַ֫חַס לִ|מְדִינוֹת כְּמוֹ פּוֹלִין."
        document.getElementById('phonemes-input').value = "mˈa ʃebahaɡdaʁˈa maʃʔˈiʁ ʔˈet hakalkalˈa hahunɡaʁˈit meʔaχˈoʁ, ʔafˈilu bejˈaχas limdinˈot kmˈo polˈin."
    }, 500);
});

// Tab switching enhancement
document.querySelectorAll('[data-bs-toggle="tab"]').forEach(tab => {
    tab.addEventListener('shown.bs.tab', function (event) {
        // Hide all status indicators and alerts when switching tabs
        document.querySelectorAll('.status-indicator').forEach(status => {
            status.style.display = 'none';
        });
        document.querySelectorAll('.alert').forEach(alert => {
            alert.style.display = 'none';
        });
    });
});


function hasDiacritics(text) {
    // Check for Hebrew diacritics (nikud) in the range \u05b0 to \u05c7
    return /[\u05b0-\u05c7]/.test(text);
}

textInput.addEventListener('keydown', (event) => {
    // Get the character that would be inserted
    const charToInsert = event.key;

    // Check if the character is a Hebrew diacritic
    // Note: event.key might not always give you the exact character for combining diacritics easily
    // This regex check is more reliable for the *content* of the text, not individual key presses
    if (charToInsert.match(/[\u05b0-\u05c7]/)) {
        event.preventDefault(); // This stops the character from being typed
        alert('Diacritics detected. These characters are not allowed in this input. Please switch to the Diacritics tab to input text with diacritics.');
        // You might want to also focus on the input if the alert takes focus away
        textInput.focus();
    }
});