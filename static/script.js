function translateText() {
  const text = document.getElementById('inputText').value;
  const languageSelect = document.getElementById('languageSelect');
  const selectedOptions = Array.from(languageSelect.selectedOptions);
  const targetLanguages = selectedOptions.map(option => option.value);

  if (targetLanguages.length === 0) {
    alert('少なくとも1つの翻訳先言語を選択してください．');
    return;
  }

  fetch('/translate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: text, target_languages: targetLanguages })
  })
  .then(response => response.json())
  .then(data => {
    const translationsDiv = document.getElementById('translations');
    translationsDiv.innerHTML = '';
    for (const [lang, translation] of Object.entries(data)) {
      const p = document.createElement('p');
      p.textContent = `${lang}: ${translation}`;
      translationsDiv.appendChild(p);

      // 音声再生
      const utterance = new SpeechSynthesisUtterance(translation);
      utterance.lang = lang;
      const playButton = document.createElement('button');
      playButton.textContent = '再生';
      playButton.onclick = () => speechSynthesis.speak(utterance);
      translationsDiv.appendChild(playButton);
    }
  });
}