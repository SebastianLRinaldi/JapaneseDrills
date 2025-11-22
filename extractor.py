"""
saves all words into a json
"""
# import requests
# from bs4 import BeautifulSoup
# import json

# # --- Get URL from user ---
# url = input("Enter the URL of the vocab table: ").strip()

# # --- Download HTML with browser-like headers ---
# headers = {
#     "User-Agent": (
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#         "AppleWebKit/537.36 (KHTML, like Gecko) "
#         "Chrome/120.0.0.0 Safari/537.36"
#     )
# }

# response = requests.get(url, headers=headers)
# response.raise_for_status()
# html = response.text

# # --- Parse HTML ---
# soup = BeautifulSoup(html, "html.parser")
# results = []

# for block in soup.select(".jukugorow"):
#     entry = {}

#     # Word + furigana
#     fc = block.select_one(".f_container")
#     if fc:
#         fu = fc.select_one(".furigana")
#         ka = fc.select_one(".f_kanji")
#         entry["word"] = ka.get_text(strip=True) if ka else ""
#         entry["furigana"] = fu.get_text(strip=True) if fu else ""

#     # JLPT
#     jlpt_span = block.select_one(".jlpt_container span")
#     if jlpt_span:
#         for c in jlpt_span.get("class", []):
#             if c.startswith("ja-jlpt_"):
#                 entry["jlpt"] = "N" + c.split("_")[1]

#     # Usefulness (UFN)
#     ufn_span = block.select_one(".ufn_container span")
#     if ufn_span:
#         for c in ufn_span.get("class", []):
#             if c.startswith("ja-ufn_"):
#                 entry["usefulness"] = int(c.split("_")[1])

#     results.append(entry)

# # --- Save to JSON ---
# output = {"vocab": results}

# with open("vocab.json", "w", encoding="utf-8") as f:
#     json.dump(output, f, ensure_ascii=False, indent=4)

# print("Saved vocab.json with", len(results), "entries.")


"""
Added a save word btn
Save just the word to json
"""
# import json
# import os
# from PyQt6.QtCore import QObject, pyqtSlot, QUrl
# from PyQt6.QtWebEngineWidgets import QWebEngineView
# from PyQt6.QtWebEngineCore import QWebEngineScript
# from PyQt6.QtWidgets import QApplication
# from PyQt6.QtWebChannel import QWebChannel

# JSON_FILE = "words.json"


# class Bridge(QObject):
#     @pyqtSlot(str)
#     def saveWord(self, word):
#         data = []

#         if os.path.exists(JSON_FILE):
#             with open(JSON_FILE, "r", encoding="utf-8") as f:
#                 data = json.load(f)

#         if word not in data:
#             data.append(word)

#         with open(JSON_FILE, "w", encoding="utf-8") as f:
#             json.dump(data, f, ensure_ascii=False, indent=2)

#         print("Saved:", word)


# class Window(QWebEngineView):
#     def __init__(self):
#         super().__init__()

#         # Bridge (Python <-> JS)
#         self.channel = QWebChannel()
#         self.bridge = Bridge()
#         self.channel.registerObject("pyBridge", self.bridge)
#         self.page().setWebChannel(self.channel)

#         # Must load qwebchannel.js before DOM runs
#         self.inject_webchannel_js()

#         # Load site
#         self.load(QUrl("https://www.kanshudo.com/collections/vocab_usefulness2021/UFN2021-1-1"))

#         # After load, inject our button script
#         self.loadFinished.connect(self.inject_button_script)

#     def inject_webchannel_js(self):
#         """Load qwebchannel.js from Qt's internal resource system."""
#         script = QWebEngineScript()
#         script.setName("qwebchannel_loader")
#         script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
#         script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
#         script.setRunsOnSubFrames(False)

#         # Load Qt's built-in qwebchannel.js
#         script.setSourceCode("""
#             var s = document.createElement("script");
#             s.src = "qrc:///qtwebchannel/qwebchannel.js";
#             document.documentElement.appendChild(s);
#         """)

#         self.page().profile().scripts().insert(script)

#     def inject_button_script(self):
#         """Injects a Save button into each vocab block after DOM is fully ready."""
#         script = """
#         function loadQWebChannelAndButtons() {
#             if (typeof QWebChannel === 'undefined') {
#                 // Inject qwebchannel.js if not loaded
#                 if (!document.getElementById('qwebchannel-js')) {
#                     var s = document.createElement('script');
#                     s.id = 'qwebchannel-js';
#                     s.src = 'qrc:///qtwebchannel/qwebchannel.js';
#                     s.onload = loadQWebChannelAndButtons;
#                     document.head.appendChild(s);
#                 }
#                 return;
#             }

#             // QWebChannel is loaded, create bridge and buttons
#             new QWebChannel(qt.webChannelTransport, function(channel) {
#                 const py = channel.objects.pyBridge;

#                 document.querySelectorAll(".jukugorow").forEach(block => {
#                     const wordEl = block.querySelector(".f_kanji");
#                     if (!wordEl) return;

#                     const word = wordEl.innerText.trim();

#                     // Avoid duplicate buttons
#                     if (block.querySelector('.save-btn')) return;

#                     const btn = document.createElement("button");
#                     btn.textContent = "Save";
#                     btn.className = "save-btn";
#                     btn.style.marginLeft = "10px";
#                     btn.style.padding = "2px 6px";

#                     btn.onclick = () => {
#                         btn.style.backgroundColor = btn.style.backgroundColor ? "" : "yellow";
#                         py.saveWord(word);
#                     };

#                     block.appendChild(btn);
#                 });
#             });
#         }

#         // Wait for DOM ready
#         if (document.readyState === "loading") {
#             document.addEventListener("DOMContentLoaded", loadQWebChannelAndButtons);
#         } else {
#             loadQWebChannelAndButtons();
#         }
#         """
#         self.page().runJavaScript(script)



# app = QApplication(["pyqt"])
# w = Window()
# w.resize(1200, 900)
# w.show()
# app.exec()


"""
Saves whole block with a btn injected
doesnt remeber saved words after shutdown or site change
can not erase words from json once added
"""
# import json
# import os
# from PyQt6.QtCore import QObject, pyqtSlot, QUrl
# from PyQt6.QtWebEngineWidgets import QWebEngineView
# from PyQt6.QtWebEngineCore import QWebEngineScript
# from PyQt6.QtWidgets import QApplication
# from PyQt6.QtWebChannel import QWebChannel

# JSON_FILE = "words.json"


# class Bridge(QObject):
#     @pyqtSlot(str)
#     def saveWord(self, json_data):
#         """Receive JSON string from JS and append it to vocab file."""
#         entry = json.loads(json_data)
#         data = []

#         if os.path.exists(JSON_FILE):
#             with open(JSON_FILE, "r", encoding="utf-8") as f:
#                 data = json.load(f)

#         # Avoid duplicates by word + furigana
#         if not any(e.get("word") == entry.get("word") and e.get("furigana") == entry.get("furigana") for e in data):
#             data.append(entry)

#         with open(JSON_FILE, "w", encoding="utf-8") as f:
#             json.dump(data, f, ensure_ascii=False, indent=2)

#         print("Saved:", entry["word"])


# class Window(QWebEngineView):
#     def __init__(self):
#         super().__init__()

#         # Bridge (Python <-> JS)
#         self.channel = QWebChannel()
#         self.bridge = Bridge()
#         self.channel.registerObject("pyBridge", self.bridge)
#         self.page().setWebChannel(self.channel)

#         # Must load qwebchannel.js before DOM runs
#         self.inject_webchannel_js()

#         # Load site
#         self.load(QUrl("https://www.kanshudo.com/collections/vocab_usefulness2021/UFN2021-1-1"))

#         # After load, inject our button script
#         self.loadFinished.connect(self.inject_button_script)

#     def inject_webchannel_js(self):
#         """Load qwebchannel.js from Qt's internal resource system."""
#         script = QWebEngineScript()
#         script.setName("qwebchannel_loader")
#         script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
#         script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
#         script.setRunsOnSubFrames(False)

#         script.setSourceCode("""
#             var s = document.createElement("script");
#             s.src = "qrc:///qtwebchannel/qwebchannel.js";
#             document.documentElement.appendChild(s);
#         """)
#         self.page().profile().scripts().insert(script)

#     def inject_button_script(self):
#         """Injects a Save button into each vocab block after DOM is fully ready."""
#         script = """
#         function loadQWebChannelAndButtons() {
#             if (typeof QWebChannel === 'undefined') {
#                 if (!document.getElementById('qwebchannel-js')) {
#                     var s = document.createElement('script');
#                     s.id = 'qwebchannel-js';
#                     s.src = 'qrc:///qtwebchannel/qwebchannel.js';
#                     s.onload = loadQWebChannelAndButtons;
#                     document.head.appendChild(s);
#                 }
#                 return;
#             }

#             new QWebChannel(qt.webChannelTransport, function(channel) {
#                 const py = channel.objects.pyBridge;

#                 document.querySelectorAll(".jukugorow").forEach(block => {
#                     const wordEl = block.querySelector(".f_kanji");
#                     if (!wordEl) return;

#                     // Avoid duplicate buttons
#                     if (block.querySelector('.save-btn')) return;

#                     const btn = document.createElement("button");
#                     btn.textContent = "Save";
#                     btn.className = "save-btn";
#                     btn.style.marginLeft = "10px";
#                     btn.style.padding = "2px 6px";

#                     btn.onclick = () => {
#                         btn.style.backgroundColor = btn.style.backgroundColor ? "" : "yellow";

#                         const entry = {
#                             word: wordEl.innerText.trim(),
#                             furigana: block.querySelector(".furigana")?.innerText.trim() || "",
#                             jlpt: block.querySelector(".jlpt_container span")?.className.match(/ja-jlpt_(\\d+)/)?.[1] ? "N" + block.querySelector(".jlpt_container span").className.match(/ja-jlpt_(\\d+)/)[1] : "",
#                             usefulness: block.querySelector(".ufn_container span")?.className.match(/ja-ufn_(\\d+)/)?.[1] ? parseInt(block.querySelector(".ufn_container span").className.match(/ja-ufn_(\\d+)/)[1]) : 0
#                         };

#                         py.saveWord(JSON.stringify(entry));
#                     };

#                     block.appendChild(btn);
#                 });
#             });
#         }

#         if (document.readyState === "loading") {
#             document.addEventListener("DOMContentLoaded", loadQWebChannelAndButtons);
#         } else {
#             loadQWebChannelAndButtons();
#         }
#         """
#         self.page().runJavaScript(script)


# if __name__ == "__main__":
#     app = QApplication(["pyqt"])
#     w = Window()
#     w.resize(1200, 900)
#     w.show()
#     app.exec()


"""
Fully works with save/unsave
is able to remember which blocks we saved based on the json
"""
# import json
# import os
# from PyQt6.QtCore import QObject, pyqtSlot, QUrl
# from PyQt6.QtWebEngineWidgets import QWebEngineView
# from PyQt6.QtWebEngineCore import QWebEngineScript
# from PyQt6.QtWidgets import QApplication
# from PyQt6.QtWebChannel import QWebChannel

# JSON_FILE = "words.json"


# class Bridge(QObject):
#     def __init__(self):
#         super().__init__()
#         # Load existing JSON once
#         self.data = []
#         if os.path.exists(JSON_FILE):
#             with open(JSON_FILE, "r", encoding="utf-8") as f:
#                 self.data = json.load(f)

#     @pyqtSlot(result=str)
#     def getSavedWords(self):
#         """Return current saved vocab as JSON string"""
#         return json.dumps(self.data)

#     @pyqtSlot(str)
#     def saveWord(self, json_data):
#         """Add a new entry to JSON if not already saved"""
#         entry = json.loads(json_data)
#         if not any(e.get("word") == entry.get("word") and e.get("furigana") == entry.get("furigana") for e in self.data):
#             self.data.append(entry)
#             self._write_json()
#             print("Saved:", entry["word"])

#     @pyqtSlot(str)
#     def removeWord(self, json_data):
#         """Remove an entry from JSON"""
#         entry = json.loads(json_data)
#         self.data = [e for e in self.data if not (e.get("word") == entry.get("word") and e.get("furigana") == entry.get("furigana"))]
#         self._write_json()
#         print("Removed:", entry["word"])

#     def _write_json(self):
#         with open(JSON_FILE, "w", encoding="utf-8") as f:
#             json.dump(self.data, f, ensure_ascii=False, indent=2)


# class Window(QWebEngineView):
#     def __init__(self):
#         super().__init__()

#         # Bridge (Python <-> JS)
#         self.channel = QWebChannel()
#         self.bridge = Bridge()
#         self.channel.registerObject("pyBridge", self.bridge)
#         self.page().setWebChannel(self.channel)

#         # Must load qwebchannel.js before DOM runs
#         self.inject_webchannel_js()

#         # Load site
#         self.load(QUrl("https://www.kanshudo.com/collections/vocab_usefulness2021/UFN2021-1-1"))

#         # After load, inject our button script
#         self.loadFinished.connect(self.inject_button_script)

#     def inject_webchannel_js(self):
#         """Load qwebchannel.js from Qt's internal resource system."""
#         script = QWebEngineScript()
#         script.setName("qwebchannel_loader")
#         script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
#         script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
#         script.setRunsOnSubFrames(False)

#         script.setSourceCode("""
#             var s = document.createElement("script");
#             s.src = "qrc:///qtwebchannel/qwebchannel.js";
#             document.documentElement.appendChild(s);
#         """)
#         self.page().profile().scripts().insert(script)

#     def inject_button_script(self):
#         """Inject Save buttons with toggle support and persistent state"""
#         script = """
#         function loadQWebChannelAndButtons() {
#             if (typeof QWebChannel === 'undefined') {
#                 if (!document.getElementById('qwebchannel-js')) {
#                     var s = document.createElement('script');
#                     s.id = 'qwebchannel-js';
#                     s.src = 'qrc:///qtwebchannel/qwebchannel.js';
#                     s.onload = loadQWebChannelAndButtons;
#                     document.head.appendChild(s);
#                 }
#                 return;
#             }

#             new QWebChannel(qt.webChannelTransport, function(channel) {
#                 const py = channel.objects.pyBridge;

#                 // Use callback to avoid Promise errors
#                 py.getSavedWords(function(savedStr) {
#                     const savedWords = JSON.parse(savedStr);

#                     document.querySelectorAll(".jukugorow").forEach(block => {
#                         const wordEl = block.querySelector(".f_kanji");
#                         if (!wordEl) return;

#                         if (block.querySelector('.save-btn')) return;

#                         const entryObj = {
#                             word: wordEl.innerText.trim(),
#                             furigana: block.querySelector(".furigana")?.innerText.trim() || "",
#                             jlpt: block.querySelector(".jlpt_container span")?.className.match(/ja-jlpt_(\\d+)/)?.[1] ? "N" + block.querySelector(".jlpt_container span").className.match(/ja-jlpt_(\\d+)/)[1] : "",
#                             usefulness: block.querySelector(".ufn_container span")?.className.match(/ja-ufn_(\\d+)/)?.[1] ? parseInt(block.querySelector(".ufn_container span").className.match(/ja-ufn_(\\d+)/)[1]) : 0
#                         };

#                         const isSaved = savedWords.some(e => e.word === entryObj.word && e.furigana === entryObj.furigana);

#                         const btn = document.createElement("button");
#                         btn.textContent = isSaved ? "Saved" : "Save";
#                         btn.className = "save-btn";
#                         btn.style.marginLeft = "10px";
#                         btn.style.padding = "2px 6px";
#                         if (isSaved) btn.style.backgroundColor = "lightgreen";

#                         btn.onclick = () => {
#                             if (btn.textContent === "Saved") {
#                                 btn.textContent = "Save";
#                                 btn.style.backgroundColor = "";
#                                 py.removeWord(JSON.stringify(entryObj));
#                             } else {
#                                 btn.textContent = "Saved";
#                                 btn.style.backgroundColor = "lightgreen";
#                                 py.saveWord(JSON.stringify(entryObj));
#                             }
#                         };

#                         block.appendChild(btn);
#                     });
#                 });
#             });
#         }

#         if (document.readyState === "loading") {
#             document.addEventListener("DOMContentLoaded", loadQWebChannelAndButtons);
#         } else {
#             loadQWebChannelAndButtons();
#         }
#         """
#         self.page().runJavaScript(script)


# if __name__ == "__main__":
#     app = QApplication(["pyqt"])
#     w = Window()
#     w.resize(1200, 900)
#     w.show()
#     app.exec()



"""
Working version with everything
sve/unsave
loaded prev entries from json to btn states
work even when going to another set of words
works with things missing furigana and jlpt lvl 
having seen if it works with missing usefulness level yet
"""
# import json
# import os
# from PyQt6.QtCore import QObject, pyqtSlot, QUrl
# from PyQt6.QtWebEngineWidgets import QWebEngineView
# from PyQt6.QtWebEngineCore import QWebEngineScript
# from PyQt6.QtWidgets import QApplication
# from PyQt6.QtWebChannel import QWebChannel

# JSON_FILE = "words.json"


# class Bridge(QObject):
#     def __init__(self):
#         super().__init__()
#         self.data = []
#         if os.path.exists(JSON_FILE):
#             with open(JSON_FILE, "r", encoding="utf-8") as f:
#                 self.data = json.load(f)

#     @pyqtSlot(result=str)
#     def getSavedWords(self):
#         return json.dumps(self.data)

#     @pyqtSlot(str, str)
#     def setWordStatus(self, json_data, status):
#         """Add/update word with status (Not Seen, Want to Know, Known)"""
#         entry = json.loads(json_data)
#         # Remove existing entry
#         self.data = [e for e in self.data if not (e.get("word") == entry.get("word") and e.get("furigana") == entry.get("furigana"))]
#         # Only add if status is not "Not Seen" (default)
#         if status != "Not Seen":
#             entry["status"] = status
#             self.data.append(entry)
#             print(f"Saved {entry['word']} as {status}")
#         else:
#             print(f"Removed {entry['word']} (Not Seen)")
#         self._write_json()

#     def _write_json(self):
#         with open(JSON_FILE, "w", encoding="utf-8") as f:
#             json.dump(self.data, f, ensure_ascii=False, indent=2)


# class Window(QWebEngineView):
#     def __init__(self):
#         super().__init__()
#         self.channel = QWebChannel()
#         self.bridge = Bridge()
#         self.channel.registerObject("pyBridge", self.bridge)
#         self.page().setWebChannel(self.channel)
#         self.inject_webchannel_js()
#         self.load(QUrl("https://www.kanshudo.com/collections/vocab_usefulness2021/UFN2021-1-1"))
#         self.loadFinished.connect(self.inject_button_script)

#     def inject_webchannel_js(self):
#         script = QWebEngineScript()
#         script.setName("qwebchannel_loader")
#         script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
#         script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
#         script.setRunsOnSubFrames(False)
#         script.setSourceCode("""
#             var s = document.createElement("script");
#             s.src = "qrc:///qtwebchannel/qwebchannel.js";
#             document.documentElement.appendChild(s);
#         """)
#         self.page().profile().scripts().insert(script)

#     def inject_button_script(self):
#         script = """
#         function loadQWebChannelAndButtons() {
#             if (typeof QWebChannel === 'undefined') {
#                 if (!document.getElementById('qwebchannel-js')) {
#                     var s = document.createElement('script');
#                     s.id = 'qwebchannel-js';
#                     s.src = 'qrc:///qtwebchannel/qwebchannel.js';
#                     s.onload = loadQWebChannelAndButtons;
#                     document.head.appendChild(s);
#                 }
#                 return;
#             }

#             new QWebChannel(qt.webChannelTransport, function(channel) {
#                 const py = channel.objects.pyBridge;

#                 py.getSavedWords(function(savedStr) {
#                     const savedWords = JSON.parse(savedStr);

#                     document.querySelectorAll(".jukugorow").forEach(block => {
#                         // Fallback: try .f_kanji first, then .jukugo
#                         const wordEl = block.querySelector(".f_kanji") || block.querySelector(".jukugo");
#                         if (!wordEl) return; // skip if no word at all

#                         if (block.querySelector('.status-btn')) return; // skip if button already exists

#                         const entryObj = {
#                             word: wordEl.innerText.trim(),
#                             furigana: block.querySelector(".furigana")?.innerText.trim() || "",
#                             jlpt: block.querySelector(".jlpt_container span")?.className.match(/ja-jlpt_(\\d+)/)?.[1] ? "N" + block.querySelector(".jlpt_container span").className.match(/ja-jlpt_(\\d+)/)[1] : "",
#                             usefulness: block.querySelector(".ufn_container span")?.className.match(/ja-ufn_(\\d+)/)?.[1] ? parseInt(block.querySelector(".ufn_container span").className.match(/ja-ufn_(\\d+)/)[1]) : 0
#                         };

#                         const savedEntry = savedWords.find(e => e.word === entryObj.word && e.furigana === entryObj.furigana);
#                         let currentStatus = savedEntry?.status || "Not Seen";

#                         const btn = document.createElement("button");
#                         btn.className = "status-btn";
#                         btn.style.marginLeft = "10px";
#                         btn.style.padding = "2px 6px";

#                         const states = ["Not Seen", "Want to Know", "Known"];

#                         function updateButton() {
#                             btn.textContent = currentStatus;
#                             if (currentStatus === "Known") btn.style.backgroundColor = "lightgreen";
#                             else if (currentStatus === "Want to Know") btn.style.backgroundColor = "lightyellow";
#                             else btn.style.backgroundColor = "";
#                         }

#                         btn.onclick = () => {
#                             const index = states.indexOf(currentStatus);
#                             currentStatus = states[(index + 1) % states.length];
#                             updateButton();
#                             py.setWordStatus(JSON.stringify(entryObj), currentStatus);
#                         };

#                         updateButton();
#                         block.appendChild(btn);
#                     });
#                 });
#             });
#         }

#         if (document.readyState === "loading") {
#             document.addEventListener("DOMContentLoaded", loadQWebChannelAndButtons);
#         } else {
#             loadQWebChannelAndButtons();
#         }
#         """
#         self.page().runJavaScript(script)



# if __name__ == "__main__":
#     app = QApplication(["pyqt"])
#     w = Window()
#     w.resize(1200, 900)
#     w.show()
#     app.exec()




"""
With a dashboard
"""
# import json
# import os
# from PyQt6.QtCore import QObject, pyqtSlot, QUrl, Qt
# from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QHBoxLayout
# from PyQt6.QtWebEngineWidgets import QWebEngineView
# from PyQt6.QtWebEngineCore import QWebEngineScript
# from PyQt6.QtWebChannel import QWebChannel

# JSON_FILE = "words.json"


# class Bridge(QObject):
#     def __init__(self):
#         super().__init__()
#         self.data = []
#         self.status_changed_callback = None  # callback to refresh dashboard
#         if os.path.exists(JSON_FILE):
#             with open(JSON_FILE, "r", encoding="utf-8") as f:
#                 self.data = json.load(f)

#     @pyqtSlot(result=str)
#     def getSavedWords(self):
#         return json.dumps(self.data)

#     @pyqtSlot(str, str)
#     def setWordStatus(self, json_data, status):
#         entry = json.loads(json_data)
#         self.data = [e for e in self.data if not (e.get("word") == entry.get("word") and e.get("furigana") == entry.get("furigana"))]
#         if status != "Not Seen":
#             entry["status"] = status
#             self.data.append(entry)
#         self._write_json()
#         if self.status_changed_callback:
#             self.status_changed_callback()

#     def _write_json(self):
#         with open(JSON_FILE, "w", encoding="utf-8") as f:
#             json.dump(self.data, f, ensure_ascii=False, indent=2)


# class Window(QWidget):
#     def __init__(self):
#         super().__init__()

#         # WebEngine
#         self.web = QWebEngineView()
#         self.channel = QWebChannel()
#         self.bridge = Bridge()
#         self.channel.registerObject("pyBridge", self.bridge)
#         self.web.page().setWebChannel(self.channel)
#         self.inject_webchannel_js()
#         self.web.load(QUrl("https://www.kanshudo.com/collections/vocab_usefulness2021/UFN2021-1-1"))
#         self.web.loadFinished.connect(self.inject_button_script)

#         # Dashboard
#         self.dashboard_known = QLabel("Known: 0")
#         self.dashboard_want = QLabel("Want to Know: 0")
#         for lbl, color in [(self.dashboard_known, "lightgreen"), (self.dashboard_want, "lightyellow")]:
#             lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
#             lbl.setStyleSheet(f"font-weight: bold; background-color: {color}; padding: 5px; border: 1px solid gray;")

#         dashboard_layout = QVBoxLayout()
#         dashboard_layout.addWidget(self.dashboard_want)
#         dashboard_layout.addWidget(self.dashboard_known)
#         dashboard_layout.addStretch()

#         # Horizontal layout: dashboard on left, web on right
#         main_layout = QHBoxLayout(self)
#         main_layout.addLayout(dashboard_layout, 0)
#         main_layout.addWidget(self.web, 1)

#         # Connect callback
#         self.bridge.status_changed_callback = self.update_dashboard
#         self.update_dashboard()  # initial update

#     def update_dashboard(self):
#         counts = {"Want to Know": 0, "Known": 0}
#         for e in self.bridge.data:
#             status = e.get("status")
#             if status in counts:
#                 counts[status] += 1
#         self.dashboard_known.setText(f"Known: {counts['Known']}")
#         self.dashboard_want.setText(f"Want to Know: {counts['Want to Know']}")

#     def inject_webchannel_js(self):
#         script = QWebEngineScript()
#         script.setName("qwebchannel_loader")
#         script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
#         script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
#         script.setRunsOnSubFrames(False)
#         script.setSourceCode("""
#             var s = document.createElement("script");
#             s.src = "qrc:///qtwebchannel/qwebchannel.js";
#             document.documentElement.appendChild(s);
#         """)
#         self.web.page().profile().scripts().insert(script)

#     def inject_button_script(self):
#         # This is your three-state toggle script from before, unchanged
#         script = """ 
#         function loadQWebChannelAndButtons() {
#             if (typeof QWebChannel === 'undefined') {
#                 if (!document.getElementById('qwebchannel-js')) {
#                     var s = document.createElement('script');
#                     s.id = 'qwebchannel-js';
#                     s.src = 'qrc:///qtwebchannel/qwebchannel.js';
#                     s.onload = loadQWebChannelAndButtons;
#                     document.head.appendChild(s);
#                 }
#                 return;
#             }

#             new QWebChannel(qt.webChannelTransport, function(channel) {
#                 const py = channel.objects.pyBridge;

#                 py.getSavedWords(function(savedStr) {
#                     const savedWords = JSON.parse(savedStr);

#                     document.querySelectorAll(".jukugorow").forEach(block => {
#                         const wordEl = block.querySelector(".f_kanji") || block.querySelector(".jukugo");
#                         if (!wordEl) return;
#                         if (block.querySelector('.status-btn')) return;

#                         const entryObj = {
#                             word: wordEl.innerText.trim(),
#                             furigana: block.querySelector(".furigana")?.innerText.trim() || "",
#                             jlpt: block.querySelector(".jlpt_container span")?.className.match(/ja-jlpt_(\\d+)/)?.[1] ? "N" + block.querySelector(".jlpt_container span").className.match(/ja-jlpt_(\\d+)/)[1] : "",
#                             usefulness: block.querySelector(".ufn_container span")?.className.match(/ja-ufn_(\\d+)/)?.[1] ? parseInt(block.querySelector(".ufn_container span").className.match(/ja-ufn_(\\d+)/)[1]) : 0
#                         };

#                         const savedEntry = savedWords.find(e => e.word === entryObj.word && e.furigana === entryObj.furigana);
#                         let currentStatus = savedEntry?.status || "Not Seen";

#                         const btn = document.createElement("button");
#                         btn.className = "status-btn";
#                         btn.style.marginLeft = "10px";
#                         btn.style.padding = "2px 6px";

#                         const states = ["Not Seen", "Want to Know", "Known"];

#                         function updateButton() {
#                             btn.textContent = currentStatus;
#                             if (currentStatus === "Known") btn.style.backgroundColor = "lightgreen";
#                             else if (currentStatus === "Want to Know") btn.style.backgroundColor = "lightyellow";
#                             else btn.style.backgroundColor = "";
#                         }

#                         btn.onclick = () => {
#                             const index = states.indexOf(currentStatus);
#                             currentStatus = states[(index + 1) % states.length];
#                             updateButton();
#                             py.setWordStatus(JSON.stringify(entryObj), currentStatus);
#                         };

#                         updateButton();
#                         block.appendChild(btn);
#                     });
#                 });
#             });
#         }

#         if (document.readyState === "loading") {
#             document.addEventListener("DOMContentLoaded", loadQWebChannelAndButtons);
#         } else {
#             loadQWebChannelAndButtons();
#         }
#         """
#         self.web.page().runJavaScript(script)


# if __name__ == "__main__":
#     app = QApplication(['pyqt'])
#     w = Window()
#     w.resize(1400, 900)
#     w.show()
#     app.exec()



"""
Whole world block changed color based on state of btn
"""
# import json
# import os
# from PyQt6.QtCore import QObject, pyqtSlot, QUrl, Qt
# from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QHBoxLayout
# from PyQt6.QtWebEngineWidgets import QWebEngineView
# from PyQt6.QtWebEngineCore import QWebEngineScript
# from PyQt6.QtWebChannel import QWebChannel

# JSON_FILE = "words.json"


# class Bridge(QObject):
#     def __init__(self):
#         super().__init__()
#         self.data = []
#         self.status_changed_callback = None  # callback to refresh dashboard
#         if os.path.exists(JSON_FILE):
#             with open(JSON_FILE, "r", encoding="utf-8") as f:
#                 self.data = json.load(f)

#     @pyqtSlot(result=str)
#     def getSavedWords(self):
#         return json.dumps(self.data)

#     @pyqtSlot(str, str)
#     def setWordStatus(self, json_data, status):
#         entry = json.loads(json_data)
#         # Remove existing entry
#         self.data = [e for e in self.data if not (e.get("word") == entry.get("word") and e.get("furigana") == entry.get("furigana"))]
#         # Add if status is not "Not Seen"
#         if status != "Not Seen":
#             entry["status"] = status
#             self.data.append(entry)
#         self._write_json()
#         # Trigger dashboard update callback
#         if self.status_changed_callback:
#             self.status_changed_callback()

#     def _write_json(self):
#         with open(JSON_FILE, "w", encoding="utf-8") as f:
#             json.dump(self.data, f, ensure_ascii=False, indent=2)


# class Window(QWidget):
#     def __init__(self):
#         super().__init__()

#         # WebEngine
#         self.web = QWebEngineView()
#         self.channel = QWebChannel()
#         self.bridge = Bridge()
#         self.channel.registerObject("pyBridge", self.bridge)
#         self.web.page().setWebChannel(self.channel)
#         self.inject_webchannel_js()
#         self.web.load(QUrl("https://www.kanshudo.com/collections/vocab_usefulness2021/UFN2021-1-1"))
#         self.web.loadFinished.connect(self.inject_button_script)

#         # Dashboard labels
#         self.dashboard_not_seen = QLabel("Not Seen: 0")
#         self.dashboard_want = QLabel("Want to Know: 0")
#         self.dashboard_known = QLabel("Known: 0")
#         for lbl, color in [
#             (self.dashboard_not_seen, "lightgray"),
#             (self.dashboard_want, "lightyellow"),
#             (self.dashboard_known, "lightgreen"),
#         ]:
#             lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
#             lbl.setStyleSheet(f"font-weight: bold; background-color: {color}; padding: 5px; border: 1px solid gray;")

#         dashboard_layout = QVBoxLayout()
#         dashboard_layout.addWidget(self.dashboard_not_seen)
#         dashboard_layout.addWidget(self.dashboard_want)
#         dashboard_layout.addWidget(self.dashboard_known)
#         dashboard_layout.addStretch()

#         # Horizontal layout: dashboard left, web right
#         main_layout = QHBoxLayout(self)
#         main_layout.addLayout(dashboard_layout, 0)
#         main_layout.addWidget(self.web, 1)

#         # Connect callback for live updates
#         self.bridge.status_changed_callback = self.update_dashboard

#         # Initial update will run after page loads
#         self.update_dashboard()

#     def update_dashboard(self):
#         # Count saved words
#         counts = {"Want to Know": 0, "Known": 0}
#         for e in self.bridge.data:
#             status = e.get("status")
#             if status in counts:
#                 counts[status] += 1

#         # JS to get total number of words on the page
#         js_total_words = "document.querySelectorAll('.jukugorow').length;"
#         def handle_total(total):
#             not_seen_count = total - counts["Want to Know"] - counts["Known"]
#             self.dashboard_not_seen.setText(f"Not Seen: {not_seen_count}")
#             self.dashboard_want.setText(f"Want to Know: {counts['Want to Know']}")
#             self.dashboard_known.setText(f"Known: {counts['Known']}")

#         self.web.page().runJavaScript(js_total_words, handle_total)

#     def inject_webchannel_js(self):
#         script = QWebEngineScript()
#         script.setName("qwebchannel_loader")
#         script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
#         script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
#         script.setRunsOnSubFrames(False)
#         script.setSourceCode("""
#             var s = document.createElement("script");
#             s.src = "qrc:///qtwebchannel/qwebchannel.js";
#             document.documentElement.appendChild(s);
#         """)
#         self.web.page().profile().scripts().insert(script)

#     def inject_button_script(self):
#         script = """
#         function loadQWebChannelAndButtons() {
#             // Wait until the DOM body exists
#             if (!document.body) {
#                 setTimeout(loadQWebChannelAndButtons, 100);
#                 return;
#             }

#             // Load qwebchannel.js if not already loaded
#             if (typeof QWebChannel === 'undefined') {
#                 if (!document.getElementById('qwebchannel-js')) {
#                     var s = document.createElement('script');
#                     s.id = 'qwebchannel-js';
#                     s.src = 'qrc:///qtwebchannel/qwebchannel.js';
#                     s.onload = loadQWebChannelAndButtons;
#                     document.head.appendChild(s);
#                 }
#                 return;
#             }

#             // Initialize QWebChannel
#             new QWebChannel(qt.webChannelTransport, function(channel) {
#                 const py = channel.objects.pyBridge;

#                 // Wait until .jukugorow elements exist
#                 function processRows() {
#                     const rows = document.querySelectorAll(".jukugorow");
#                     if (!rows.length) {
#                         setTimeout(processRows, 200);
#                         return;
#                     }

#                     // Fetch saved words from Python
#                     py.getSavedWords(function(savedStr) {
#                         const savedWords = JSON.parse(savedStr);

#                         rows.forEach(block => {
#                             const wordEl = block.querySelector(".f_kanji") || block.querySelector(".jukugo");
#                             if (!wordEl) return;
#                             if (block.querySelector('.status-btn')) return;

#                             const entryObj = {
#                                 word: wordEl.innerText.trim(),
#                                 furigana: block.querySelector(".furigana")?.innerText.trim() || "",
#                                 jlpt: block.querySelector(".jlpt_container span")?.className.match(/ja-jlpt_(\\d+)/)?.[1] ? "N" + block.querySelector(".jlpt_container span").className.match(/ja-jlpt_(\\d+)/)[1] : "",
#                                 usefulness: block.querySelector(".ufn_container span")?.className.match(/ja-ufn_(\\d+)/)?.[1] ? parseInt(block.querySelector(".ufn_container span").className.match(/ja-ufn_(\\d+)/)[1]) : 0
#                             };

#                             const savedEntry = savedWords.find(e => e.word === entryObj.word && e.furigana === entryObj.furigana);
#                             let currentStatus = savedEntry?.status || "Not Seen";

#                             const btn = document.createElement("button");
#                             btn.className = "status-btn";
#                             btn.style.marginLeft = "10px";
#                             btn.style.padding = "2px 6px";

#                             const states = ["Not Seen", "Want to Know", "Known"];

#                             function updateButtonAndRow() {
#                                 btn.textContent = currentStatus;
#                                 // Button color
#                                 if (currentStatus === "Known") btn.style.backgroundColor = "lightgreen";
#                                 else if (currentStatus === "Want to Know") btn.style.backgroundColor = "lightyellow";
#                                 else btn.style.backgroundColor = "";

#                                 // Row background color
#                                 if (currentStatus === "Known") block.style.backgroundColor = "#d4f8d4";      // light green
#                                 else if (currentStatus === "Want to Know") block.style.backgroundColor = "#fff5b1"; // light yellow
#                                 else block.style.backgroundColor = "#f0f0f0"; // gray
#                             }

#                             btn.onclick = () => {
#                                 const index = states.indexOf(currentStatus);
#                                 currentStatus = states[(index + 1) % states.length];
#                                 updateButtonAndRow();
#                                 py.setWordStatus(JSON.stringify(entryObj), currentStatus);
#                             };

#                             updateButtonAndRow();
#                             block.appendChild(btn);
#                         });
#                     });
#                 }

#                 processRows();
#             });
#         }

#         // Ensure it runs once the DOM is ready
#         if (document.readyState === "loading") {
#             document.addEventListener("DOMContentLoaded", loadQWebChannelAndButtons);
#         } else {
#             loadQWebChannelAndButtons();
#         }
#         """
#         self.web.page().runJavaScript(script)


# if __name__ == "__main__":
#     app = QApplication(['pyqt'])
#     w = Window()
#     w.resize(1400, 900)
#     w.show()
#     app.exec()


"""
Not seen in dashboard is can not go lower than 0 fixed the math
"""
# import json
# import os
# from PyQt6.QtCore import QObject, pyqtSlot, QUrl, Qt
# from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QHBoxLayout
# from PyQt6.QtWebEngineWidgets import QWebEngineView
# from PyQt6.QtWebEngineCore import QWebEngineScript
# from PyQt6.QtWebChannel import QWebChannel

# JSON_FILE = "words.json"


# class Bridge(QObject):
#     def __init__(self):
#         super().__init__()
#         self.data = []
#         self.status_changed_callback = None
#         if os.path.exists(JSON_FILE):
#             with open(JSON_FILE, "r", encoding="utf-8") as f:
#                 self.data = json.load(f)

#     @pyqtSlot(result=str)
#     def getSavedWords(self):
#         return json.dumps(self.data)

#     @pyqtSlot(str, str)
#     def setWordStatus(self, json_data, status):
#         entry = json.loads(json_data)
#         # Remove existing entry
#         self.data = [e for e in self.data if not (e.get("word") == entry.get("word") and e.get("furigana") == entry.get("furigana"))]
#         # Add if status is not "Not Seen"
#         if status != "Not Seen":
#             entry["status"] = status
#             self.data.append(entry)
#         self._write_json()
#         # Trigger dashboard update
#         if self.status_changed_callback:
#             self.status_changed_callback()

#     def _write_json(self):
#         with open(JSON_FILE, "w", encoding="utf-8") as f:
#             json.dump(self.data, f, ensure_ascii=False, indent=2)


# class Window(QWidget):
#     def __init__(self):
#         super().__init__()

#         # WebEngine
#         self.web = QWebEngineView()
#         self.channel = QWebChannel()
#         self.bridge = Bridge()
#         self.channel.registerObject("pyBridge", self.bridge)
#         self.web.page().setWebChannel(self.channel)
#         self.inject_webchannel_js()
#         self.web.load(QUrl("https://www.kanshudo.com/collections/vocab_usefulness2021/UFN2021-1-1"))
#         self.web.loadFinished.connect(self.inject_button_script)

#         # Dashboard labels
#         self.dashboard_not_seen = QLabel("Not Seen: 0")
#         self.dashboard_want = QLabel("Want to Know: 0")
#         self.dashboard_known = QLabel("Known: 0")
#         for lbl, color in [
#             (self.dashboard_not_seen, "lightgray"),
#             (self.dashboard_want, "lightyellow"),
#             (self.dashboard_known, "lightgreen"),
#         ]:
#             lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
#             lbl.setStyleSheet(f"font-weight: bold; background-color: {color}; padding: 5px; border: 1px solid gray;")

#         dashboard_layout = QVBoxLayout()
#         dashboard_layout.addWidget(self.dashboard_not_seen)
#         dashboard_layout.addWidget(self.dashboard_want)
#         dashboard_layout.addWidget(self.dashboard_known)
#         dashboard_layout.addStretch()

#         # Horizontal layout: dashboard left, web right
#         main_layout = QHBoxLayout(self)
#         main_layout.addLayout(dashboard_layout, 0)
#         main_layout.addWidget(self.web, 1)

#         # Connect callback for live updates
#         self.bridge.status_changed_callback = self.update_dashboard

#         # Initial update will run after page loads
#         self.update_dashboard()

#     def update_dashboard(self):
#         # Count saved words
#         counts = {"Want to Know": 0, "Known": 0}
#         for e in self.bridge.data:
#             status = e.get("status")
#             if status in counts:
#                 counts[status] += 1

#         # JS to count blocks that have a word
#         js_total_words = """
#             Array.from(document.querySelectorAll('.jukugorow'))
#                 .filter(block => block.querySelector('.f_kanji') || block.querySelector('.jukugo'))
#                 .length;
#         """

#         def handle_total(total):
#             not_seen_count = total - counts["Want to Know"] - counts["Known"]
#             not_seen_count = max(not_seen_count, 0)
#             self.dashboard_not_seen.setText(f"Not Seen: {not_seen_count}")
#             self.dashboard_want.setText(f"Want to Know: {counts['Want to Know']}")
#             self.dashboard_known.setText(f"Known: {counts['Known']}")

#         self.web.page().runJavaScript(js_total_words, handle_total)

#     def inject_webchannel_js(self):
#         script = QWebEngineScript()
#         script.setName("qwebchannel_loader")
#         script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
#         script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
#         script.setRunsOnSubFrames(False)
#         script.setSourceCode("""
#             var s = document.createElement("script");
#             s.src = "qrc:///qtwebchannel/qwebchannel.js";
#             document.documentElement.appendChild(s);
#         """)
#         self.web.page().profile().scripts().insert(script)

#     def inject_button_script(self):
#         script = """
#         function loadQWebChannelAndButtons() {
#             if (!document.body) {
#                 setTimeout(loadQWebChannelAndButtons, 100);
#                 return;
#             }

#             if (typeof QWebChannel === 'undefined') {
#                 if (!document.getElementById('qwebchannel-js')) {
#                     var s = document.createElement('script');
#                     s.id = 'qwebchannel-js';
#                     s.src = 'qrc:///qtwebchannel/qwebchannel.js';
#                     s.onload = loadQWebChannelAndButtons;
#                     document.head.appendChild(s);
#                 }
#                 return;
#             }

#             new QWebChannel(qt.webChannelTransport, function(channel) {
#                 const py = channel.objects.pyBridge;

#                 function processRows() {
#                     const rows = document.querySelectorAll(".jukugorow");
#                     if (!rows.length) {
#                         setTimeout(processRows, 200);
#                         return;
#                     }

#                     py.getSavedWords(function(savedStr) {
#                         const savedWords = JSON.parse(savedStr);

#                         rows.forEach(block => {
#                             const wordEl = block.querySelector(".f_kanji") || block.querySelector(".jukugo");
#                             if (!wordEl) return;
#                             if (block.querySelector('.status-btn')) return;

#                             const entryObj = {
#                                 word: wordEl.innerText.trim(),
#                                 furigana: block.querySelector(".furigana")?.innerText.trim() || "",
#                                 jlpt: block.querySelector(".jlpt_container span")?.className.match(/ja-jlpt_(\\d+)/)?.[1] ? "N" + block.querySelector(".jlpt_container span").className.match(/ja-jlpt_(\\d+)/)[1] : "",
#                                 usefulness: block.querySelector(".ufn_container span")?.className.match(/ja-ufn_(\\d+)/)?.[1] ? parseInt(block.querySelector(".ufn_container span").className.match(/ja-ufn_(\\d+)/)[1]) : 0
#                             };

#                             const savedEntry = savedWords.find(e => e.word === entryObj.word && e.furigana === entryObj.furigana);
#                             let currentStatus = savedEntry?.status || "Not Seen";

#                             const btn = document.createElement("button");
#                             btn.className = "status-btn";
#                             btn.style.marginLeft = "10px";
#                             btn.style.padding = "2px 6px";

#                             const states = ["Not Seen", "Want to Know", "Known"];

#                             function updateButtonAndRow() {
#                                 btn.textContent = currentStatus;
#                                 if (currentStatus === "Known") btn.style.backgroundColor = "lightgreen";
#                                 else if (currentStatus === "Want to Know") btn.style.backgroundColor = "lightyellow";
#                                 else btn.style.backgroundColor = "";

#                                 if (currentStatus === "Known") block.style.backgroundColor = "#d4f8d4";
#                                 else if (currentStatus === "Want to Know") block.style.backgroundColor = "#fff5b1";
#                                 else block.style.backgroundColor = "#f0f0f0";
#                             }

#                             btn.onclick = () => {
#                                 const index = states.indexOf(currentStatus);
#                                 currentStatus = states[(index + 1) % states.length];
#                                 updateButtonAndRow();
#                                 py.setWordStatus(JSON.stringify(entryObj), currentStatus);
#                             };

#                             updateButtonAndRow();
#                             block.appendChild(btn);
#                         });
#                     });
#                 }

#                 processRows();
#             });
#         }

#         if (document.readyState === "loading") {
#             document.addEventListener("DOMContentLoaded", loadQWebChannelAndButtons);
#         } else {
#             loadQWebChannelAndButtons();
#         }
#         """
#         self.web.page().runJavaScript(script)


# if __name__ == "__main__":
#     app = QApplication(['pyqt'])
#     w = Window()
#     w.resize(1400, 900)
#     w.show()
#     app.exec()



"""
Correct working version with unseen count
- dashboard
- save/unsave
- load in want to know and known words from json
- block changes color based on state of btn
- works even when going to another table url
- fixed weird json saving just partial words
"""
# import json
# import os
# from PyQt6.QtCore import QObject, pyqtSlot, QUrl, Qt
# from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QHBoxLayout
# from PyQt6.QtWebEngineWidgets import QWebEngineView
# from PyQt6.QtWebEngineCore import QWebEngineScript
# from PyQt6.QtWebChannel import QWebChannel

# JSON_FILE = "words.json"


# class Bridge(QObject):
#     def __init__(self):
#         super().__init__()
#         self.data = []
#         self.status_changed_callback = None
#         self.parent_window = None
#         if os.path.exists(JSON_FILE):
#             with open(JSON_FILE, "r", encoding="utf-8") as f:
#                 self.data = json.load(f)

#     @pyqtSlot(result=str)
#     def getSavedWords(self):
#         return json.dumps(self.data)

#     @pyqtSlot(str, str)
#     def setWordStatus(self, json_data, status):
#         entry = json.loads(json_data)
#         # Remove existing entry
#         self.data = [e for e in self.data if not (e.get("word") == entry.get("word") and e.get("furigana") == entry.get("furigana"))]
#         # Add if status is not "Not Seen"
#         if status != "Not Seen":
#             entry["status"] = status
#             self.data.append(entry)
#         self._write_json()
#         # Trigger dashboard update
#         if self.status_changed_callback:
#             self.status_changed_callback()

#     @pyqtSlot()
#     def updateNotSeenDashboard(self):
#         if self.parent_window:
#             self.parent_window.update_dashboard()

#     def _write_json(self):
#         with open(JSON_FILE, "w", encoding="utf-8") as f:
#             json.dump(self.data, f, ensure_ascii=False, indent=2)


# class Window(QWidget):
#     def __init__(self):
#         super().__init__()

#         # WebEngine
#         self.web = QWebEngineView()
#         self.channel = QWebChannel()
#         self.bridge = Bridge()
#         self.bridge.parent_window = self
#         self.channel.registerObject("pyBridge", self.bridge)
#         self.web.page().setWebChannel(self.channel)
#         self.inject_webchannel_js()
#         self.web.load(QUrl("https://www.kanshudo.com/collections/vocab_usefulness2021/UFN2021-1-1"))
#         self.web.loadFinished.connect(self.inject_button_script)

#         # Dashboard labels
#         self.dashboard_not_seen = QLabel("Not Seen: 0")
#         self.dashboard_want = QLabel("Want to Know: 0")
#         self.dashboard_known = QLabel("Known: 0")
#         for lbl, color in [
#             (self.dashboard_not_seen, "lightgray"),
#             (self.dashboard_want, "lightyellow"),
#             (self.dashboard_known, "lightgreen"),
#         ]:
#             lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
#             lbl.setStyleSheet(f"font-weight: bold; background-color: {color}; padding: 5px; border: 1px solid gray;")

#         dashboard_layout = QVBoxLayout()
#         dashboard_layout.addWidget(self.dashboard_not_seen)
#         dashboard_layout.addWidget(self.dashboard_want)
#         dashboard_layout.addWidget(self.dashboard_known)
#         dashboard_layout.addStretch()

#         # Horizontal layout: dashboard left, web right
#         main_layout = QHBoxLayout(self)
#         main_layout.addLayout(dashboard_layout, 0)
#         main_layout.addWidget(self.web, 1)

#         # Connect callback for live updates
#         self.bridge.status_changed_callback = self.update_dashboard

#         # Initial dashboard update
#         self.update_dashboard()

#     def update_dashboard(self):
#         # Count saved words
#         counts = {"Want to Know": 0, "Known": 0}
#         for e in self.bridge.data:
#             status = e.get("status")
#             if status in counts:
#                 counts[status] += 1

#         # JS to count the number of buttons currently in 'Not Seen' state
#         js_not_seen = """
#             Array.from(document.querySelectorAll('.status-btn'))
#                 .filter(btn => btn.textContent.trim() === 'Not Seen')
#                 .length;
#         """

#         def handle_not_seen(not_seen_count):
#             self.dashboard_not_seen.setText(f"Not Seen: {not_seen_count}")
#             self.dashboard_want.setText(f"Want to Know: {counts['Want to Know']}")
#             self.dashboard_known.setText(f"Known: {counts['Known']}")

#         self.web.page().runJavaScript(js_not_seen, handle_not_seen)

#     def inject_webchannel_js(self):
#         script = QWebEngineScript()
#         script.setName("qwebchannel_loader")
#         script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
#         script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
#         script.setRunsOnSubFrames(False)
#         script.setSourceCode("""
#             var s = document.createElement("script");
#             s.src = "qrc:///qtwebchannel/qwebchannel.js";
#             document.documentElement.appendChild(s);
#         """)
#         self.web.page().profile().scripts().insert(script)

#     def inject_button_script(self):
#         script = r"""
#         function loadQWebChannelAndButtons() {
#             if (!document.body) {
#                 setTimeout(loadQWebChannelAndButtons, 100);
#                 return;
#             }

#             if (typeof QWebChannel === 'undefined') {
#                 if (!document.getElementById('qwebchannel-js')) {
#                     var s = document.createElement('script');
#                     s.id = 'qwebchannel-js';
#                     s.src = 'qrc:///qtwebchannel/qwebchannel.js';
#                     s.onload = loadQWebChannelAndButtons;
#                     document.head.appendChild(s);
#                 }
#                 return;
#             }

#             new QWebChannel(qt.webChannelTransport, function(channel) {
#                 const py = channel.objects.pyBridge;

#                 function processRows() {
#                     const rows = document.querySelectorAll(".jukugorow");
#                     if (!rows.length) {
#                         setTimeout(processRows, 200);
#                         return;
#                     }

#                     py.getSavedWords(function(savedStr) {
#                         const savedWords = JSON.parse(savedStr);

#                         rows.forEach(block => {
#                             const anchor = block.querySelector("a");
#                             if (!anchor || block.querySelector('.status-btn')) return;

#                             // --- Extract word (kanji + extra kana outside f_container) ---
#                             let word = "";
#                             anchor.childNodes.forEach(node => {
#                                 if (node.nodeType === Node.ELEMENT_NODE && node.classList.contains("f_container")) {
#                                     const kanji = node.querySelector(".f_kanji")?.innerText || "";
#                                     word += kanji;
#                                 } else if (node.nodeType === Node.TEXT_NODE) {
#                                     word += node.textContent;
#                                 }
#                             });
#                             word = word.trim();

#                             // --- Extract furigana (furigana + extra kana outside f_container) ---
#                             let furigana = "";
#                             anchor.childNodes.forEach(node => {
#                                 if (node.nodeType === Node.ELEMENT_NODE && node.classList.contains("f_container")) {
#                                     const f = node.querySelector(".furigana")?.innerText || "";
#                                     furigana += f;
#                                 } else if (node.nodeType === Node.TEXT_NODE) {
#                                     furigana += node.textContent;
#                                 }
#                             });
#                             furigana = furigana.trim();

#                             // Fallback: if no kanji (pure kana word)
#                             if (!word) word = furigana;

#                             const entryObj = {
#                                 word: word,
#                                 furigana: furigana,
#                                 jlpt: block.querySelector(".jlpt_container span")?.className.match(/ja-jlpt_(\d+)/)?.[1] ? "N" + block.querySelector(".jlpt_container span").className.match(/ja-jlpt_(\d+)/)[1] : "",
#                                 usefulness: block.querySelector(".ufn_container span")?.className.match(/ja-ufn_(\d+)/)?.[1] ? parseInt(block.querySelector(".ufn_container span").className.match(/ja-ufn_(\d+)/)[1]) : 0
#                             };

#                             const savedEntry = savedWords.find(e => e.word === entryObj.word && e.furigana === entryObj.furigana);
#                             let currentStatus = savedEntry?.status || "Not Seen";

#                             const btn = document.createElement("button");
#                             btn.className = "status-btn";
#                             btn.style.marginLeft = "10px";
#                             btn.style.padding = "2px 6px";

#                             const states = ["Not Seen", "Want to Know", "Known"];

#                             function updateButtonAndRow() {
#                                 btn.textContent = currentStatus;
#                                 if (currentStatus === "Known") btn.style.backgroundColor = "lightgreen";
#                                 else if (currentStatus === "Want to Know") btn.style.backgroundColor = "lightyellow";
#                                 else btn.style.backgroundColor = "";

#                                 if (currentStatus === "Known") block.style.backgroundColor = "#d4f8d4";
#                                 else if (currentStatus === "Want to Know") block.style.backgroundColor = "#fff5b1";
#                                 else block.style.backgroundColor = "#f0f0f0";
#                             }

#                             btn.onclick = () => {
#                                 const index = states.indexOf(currentStatus);
#                                 currentStatus = states[(index + 1) % states.length];
#                                 updateButtonAndRow();
#                                 py.setWordStatus(JSON.stringify(entryObj), currentStatus);
#                             };

#                             updateButtonAndRow();
#                             block.appendChild(btn);
#                         });

#                         // Notify Python to update Not Seen dashboard
#                         if (py.updateNotSeenDashboard) {
#                             py.updateNotSeenDashboard();
#                         }
#                     });
#                 }

#                 processRows();
#             });
#         }

#         if (document.readyState === "loading") {
#             document.addEventListener("DOMContentLoaded", loadQWebChannelAndButtons);
#         } else {
#             loadQWebChannelAndButtons();
#         }
#         """
#         self.web.page().runJavaScript(script)


# if __name__ == "__main__":
#     app = QApplication(['pyqt'])
#     w = Window()
#     w.resize(1400, 900)
#     w.show()
#     app.exec()













"""
Full working version with better dashboard for sheet searching
"""
# import json
# import os
# from PyQt6.QtCore import *
# from PyQt6.QtWidgets import * 
# from PyQt6.QtGui import *
# from PyQt6.QtWebEngineWidgets import QWebEngineView
# from PyQt6.QtWebEngineCore import QWebEngineScript
# from PyQt6.QtWebChannel import QWebChannel

# JSON_FILE = "words.json"


# class Bridge(QObject):
#     def __init__(self):
#         super().__init__()
#         self.data = []
#         self.status_changed_callback = None
#         self.parent_window = None
#         if os.path.exists(JSON_FILE):
#             with open(JSON_FILE, "r", encoding="utf-8") as f:
#                 self.data = json.load(f)

#     @pyqtSlot(result=str)
#     def getSavedWords(self):
#         return json.dumps(self.data)

#     @pyqtSlot(str, str)
#     def setWordStatus(self, json_data, status):
#         entry = json.loads(json_data)
#         # Remove existing entry
#         self.data = [e for e in self.data if not (e.get("word") == entry.get("word") and e.get("furigana") == entry.get("furigana"))]
#         # Add if status is not "Not Seen"
#         if status != "Not Seen":
#             entry["status"] = status
#             self.data.append(entry)
#         self._write_json()
#         # Trigger dashboard update
#         if self.status_changed_callback:
#             self.status_changed_callback()

#     @pyqtSlot()
#     def updateNotSeenDashboard(self):
#         if self.parent_window:
#             self.parent_window.update_dashboard()

#     def _write_json(self):
#         with open(JSON_FILE, "w", encoding="utf-8") as f:
#             json.dump(self.data, f, ensure_ascii=False, indent=2)


# class Window(QWidget):
#     LEVEL_CONFIG = {
#         1: {"words": 500, "step": 100},
#         2: {"words": 1000, "step": 100},
#         3: {"words": 1500, "step": 100},
#         4: {"words": 2000, "step": 100},
#         5: {"words": 5000, "step": 100},
#     }

#     BASE_URL = "https://www.kanshudo.com/collections/vocab_usefulness2021/UFN2021"

#     def __init__(self):
#         super().__init__()

#         # WebEngine
#         self.web = QWebEngineView()
#         self.channel = QWebChannel()
#         self.bridge = Bridge()
#         self.bridge.parent_window = self
#         self.channel.registerObject("pyBridge", self.bridge)
#         self.web.page().setWebChannel(self.channel)
#         self.inject_webchannel_js()

#         # Initial load: Level 1, first page
#         first_level = "Level 1 (500 words)"
#         self.web.load(QUrl(f"{self.BASE_URL}-1-1"))
#         self.web.loadFinished.connect(self.inject_button_script)

#         # Dashboard labels
#         self.dashboard_not_seen = QLabel("Not Seen: 0")
#         self.dashboard_want = QLabel("Want to Know: 0")
#         self.dashboard_known = QLabel("Known: 0")
#         for lbl, color in [
#             (self.dashboard_not_seen, "lightgray"),
#             (self.dashboard_want, "lightyellow"),
#             (self.dashboard_known, "lightgreen"),
#         ]:
#             lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
#             lbl.setStyleSheet(f"font-weight: bold; background-color: {color}; padding: 5px; border: 1px solid gray;")

#         # Level dropdown
#         self.level_dropdown = QComboBox()
#         self.level_dropdown.addItems([f"Level {lvl} ({cfg['words']} words)" for lvl, cfg in self.LEVEL_CONFIG.items()])
#         self.level_dropdown.currentTextChanged.connect(self.on_level_changed)

#         # Page dropdown
#         self.page_dropdown = QComboBox()
#         self.page_dropdown.currentTextChanged.connect(self.on_page_changed)
#         self.update_page_dropdown(first_level)

#         # Dashboard layout
#         dashboard_layout = QVBoxLayout()
#         dashboard_layout.addWidget(QLabel("Level:"))
#         dashboard_layout.addWidget(self.level_dropdown)
#         dashboard_layout.addWidget(QLabel("Page:"))
#         dashboard_layout.addWidget(self.page_dropdown)
#         dashboard_layout.addWidget(self.dashboard_not_seen)
#         dashboard_layout.addWidget(self.dashboard_want)
#         dashboard_layout.addWidget(self.dashboard_known)
#         dashboard_layout.addStretch()

#         # Main layout
#         main_layout = QHBoxLayout(self)
#         main_layout.addLayout(dashboard_layout, 0)
#         main_layout.addWidget(self.web, 1)

#         # Connect callback for live updates
#         self.bridge.status_changed_callback = self.update_dashboard
#         self.update_dashboard()

#     def update_page_dropdown(self, level_name):
#         """Generate page ranges and URLs for the dropdown based on level"""
#         self.page_dropdown.blockSignals(True)
#         self.page_dropdown.clear()

#         # Extract level number from text
#         level_num = int(level_name.split()[1])
#         config = self.LEVEL_CONFIG[level_num]
#         step = config["step"]
#         total_words = config["words"]

#         ranges = []
#         urls = []

#         # First page always ends with -1
#         ranges.append(f"1-{min(step, total_words)}")
#         urls.append(f"{self.BASE_URL}-{level_num}-1")

#         # Subsequent pages
#         for start in range(1 + step, total_words + 1, step):
#             end = min(start + step - 1, total_words)
#             ranges.append(f"{start}-{end}")
#             urls.append(f"{self.BASE_URL}-{level_num}-{start}")

#         # Populate dropdown
#         for range_label, url in zip(ranges, urls):
#             self.page_dropdown.addItem(range_label, url)

#         self.page_dropdown.setCurrentIndex(0)
#         self.page_dropdown.blockSignals(False)

#     def on_level_changed(self, level_name):
#         self.update_page_dropdown(level_name)
#         # Load first page of the selected level
#         first_url = self.page_dropdown.itemData(0)
#         if first_url:
#             self.web.load(QUrl(first_url))

#     def on_page_changed(self, _):
#         url = self.page_dropdown.currentData()
#         if url:
#             self.web.load(QUrl(url))

#     def update_dashboard(self):
#         # Count saved words
#         counts = {"Want to Know": 0, "Known": 0}
#         for e in self.bridge.data:
#             status = e.get("status")
#             if status in counts:
#                 counts[status] += 1

#         # JS to count the number of buttons currently in 'Not Seen' state
#         js_not_seen = """
#             Array.from(document.querySelectorAll('.status-btn'))
#                 .filter(btn => btn.textContent.trim() === 'Not Seen')
#                 .length;
#         """

#         def handle_not_seen(not_seen_count):
#             self.dashboard_not_seen.setText(f"Not Seen: {not_seen_count}")
#             self.dashboard_want.setText(f"Want to Know: {counts['Want to Know']}")
#             self.dashboard_known.setText(f"Known: {counts['Known']}")

#         self.web.page().runJavaScript(js_not_seen, handle_not_seen)

#     def inject_webchannel_js(self):
#         script = QWebEngineScript()
#         script.setName("qwebchannel_loader")
#         script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
#         script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
#         script.setRunsOnSubFrames(False)
#         script.setSourceCode("""
#             var s = document.createElement("script");
#             s.src = "qrc:///qtwebchannel/qwebchannel.js";
#             document.documentElement.appendChild(s);
#         """)
#         self.web.page().profile().scripts().insert(script)

#     def inject_button_script(self):
#         script = r"""
#         function loadQWebChannelAndButtons() {
#             if (!document.body) {
#                 setTimeout(loadQWebChannelAndButtons, 100);
#                 return;
#             }

#             if (typeof QWebChannel === 'undefined') {
#                 if (!document.getElementById('qwebchannel-js')) {
#                     var s = document.createElement('script');
#                     s.id = 'qwebchannel-js';
#                     s.src = 'qrc:///qtwebchannel/qwebchannel.js';
#                     s.onload = loadQWebChannelAndButtons;
#                     document.head.appendChild(s);
#                 }
#                 return;
#             }

#             new QWebChannel(qt.webChannelTransport, function(channel) {
#                 const py = channel.objects.pyBridge;

#                 function processRows() {
#                     const rows = document.querySelectorAll(".jukugorow");
#                     if (!rows.length) {
#                         setTimeout(processRows, 200);
#                         return;
#                     }

#                     py.getSavedWords(function(savedStr) {
#                         const savedWords = JSON.parse(savedStr);

#                         rows.forEach(block => {
#                             const anchor = block.querySelector("a");
#                             if (!anchor || block.querySelector('.status-btn')) return;

#                             // --- Extract word (kanji + extra kana outside f_container) ---
#                             let word = "";
#                             anchor.childNodes.forEach(node => {
#                                 if (node.nodeType === Node.ELEMENT_NODE && node.classList.contains("f_container")) {
#                                     const kanji = node.querySelector(".f_kanji")?.innerText || "";
#                                     word += kanji;
#                                 } else if (node.nodeType === Node.TEXT_NODE) {
#                                     word += node.textContent;
#                                 }
#                             });
#                             word = word.trim();

#                             // --- Extract furigana (furigana + extra kana outside f_container) ---
#                             let furigana = "";
#                             anchor.childNodes.forEach(node => {
#                                 if (node.nodeType === Node.ELEMENT_NODE && node.classList.contains("f_container")) {
#                                     const f = node.querySelector(".furigana")?.innerText || "";
#                                     furigana += f;
#                                 } else if (node.nodeType === Node.TEXT_NODE) {
#                                     furigana += node.textContent;
#                                 }
#                             });
#                             furigana = furigana.trim();

#                             // Fallback: if no kanji (pure kana word)
#                             if (!word) word = furigana;

#                             const entryObj = {
#                                 word: word,
#                                 furigana: furigana,
#                                 jlpt: block.querySelector(".jlpt_container span")?.className.match(/ja-jlpt_(\d+)/)?.[1] ? "N" + block.querySelector(".jlpt_container span").className.match(/ja-jlpt_(\d+)/)[1] : "",
#                                 usefulness: block.querySelector(".ufn_container span")?.className.match(/ja-ufn_(\d+)/)?.[1] ? parseInt(block.querySelector(".ufn_container span").className.match(/ja-ufn_(\d+)/)[1]) : 0
#                             };

#                             const savedEntry = savedWords.find(e => e.word === entryObj.word && e.furigana === entryObj.furigana);
#                             let currentStatus = savedEntry?.status || "Not Seen";

#                             const btn = document.createElement("button");
#                             btn.className = "status-btn";
#                             btn.style.marginLeft = "10px";
#                             btn.style.padding = "2px 6px";

#                             const states = ["Not Seen", "Want to Know", "Known"];

#                             function updateButtonAndRow() {
#                                 btn.textContent = currentStatus;
#                                 if (currentStatus === "Known") btn.style.backgroundColor = "lightgreen";
#                                 else if (currentStatus === "Want to Know") btn.style.backgroundColor = "lightyellow";
#                                 else btn.style.backgroundColor = "";

#                                 if (currentStatus === "Known") block.style.backgroundColor = "#d4f8d4";
#                                 else if (currentStatus === "Want to Know") block.style.backgroundColor = "#fff5b1";
#                                 else block.style.backgroundColor = "#f0f0f0";
#                             }

#                             btn.onclick = () => {
#                                 const index = states.indexOf(currentStatus);
#                                 currentStatus = states[(index + 1) % states.length];
#                                 updateButtonAndRow();
#                                 py.setWordStatus(JSON.stringify(entryObj), currentStatus);
#                             };

#                             updateButtonAndRow();
#                             block.appendChild(btn);
#                         });

#                         // Notify Python to update Not Seen dashboard
#                         if (py.updateNotSeenDashboard) {
#                             py.updateNotSeenDashboard();
#                         }
#                     });
#                 }

#                 processRows();
#             });
#         }

#         if (document.readyState === "loading") {
#             document.addEventListener("DOMContentLoaded", loadQWebChannelAndButtons);
#         } else {
#             loadQWebChannelAndButtons();
#         }
#         """
#         self.web.page().runJavaScript(script)


# if __name__ == "__main__":
#     app = QApplication(['pyqt'])
#     w = Window()
#     w.resize(1400, 900)
#     w.show()
#     app.exec()



























"""
Everything works perfectly
- added in a "will not add" for a anki btn state
"""
# import json
# import os
# from PyQt6.QtCore import *
# from PyQt6.QtWidgets import * 
# from PyQt6.QtGui import *
# from PyQt6.QtWebEngineWidgets import QWebEngineView
# from PyQt6.QtWebEngineCore import QWebEngineScript
# from PyQt6.QtWebChannel import QWebChannel

# JSON_FILE = "words.json"


# class Bridge(QObject):
#     def __init__(self):
#         super().__init__()
#         self.data = []
#         self.status_changed_callback = None
#         self.parent_window = None
#         if os.path.exists(JSON_FILE):
#             with open(JSON_FILE, "r", encoding="utf-8") as f:
#                 self.data = json.load(f)

#     @pyqtSlot(result=str)
#     def getSavedWords(self):
#         return json.dumps(self.data)

#     @pyqtSlot(str, str)
#     def setWordStatus(self, json_data, status):
#         entry = json.loads(json_data)
#         # Remove existing entry
#         self.data = [e for e in self.data if not (e.get("word") == entry.get("word") and e.get("furigana") == entry.get("furigana"))]
#         # Add if status is not "Not Seen"
#         if status != "Not Seen":
#             entry["status"] = status
#             self.data.append(entry)
#         self._write_json()
#         # Trigger dashboard update
#         if self.status_changed_callback:
#             self.status_changed_callback()

#     @pyqtSlot()
#     def updateNotSeenDashboard(self):
#         if self.parent_window:
#             self.parent_window.update_dashboard()

#     def _write_json(self):
#         with open(JSON_FILE, "w", encoding="utf-8") as f:
#             json.dump(self.data, f, ensure_ascii=False, indent=2)


# class Window(QWidget):
#     LEVEL_CONFIG = {
#         1: {"words": 500, "step": 100},
#         2: {"words": 1000, "step": 100},
#         3: {"words": 1500, "step": 100},
#         4: {"words": 2000, "step": 100},
#         5: {"words": 5000, "step": 100},
#     }

#     BASE_URL = "https://www.kanshudo.com/collections/vocab_usefulness2021/UFN2021"

#     def __init__(self):
#         super().__init__()

#         # WebEngine setup
#         self.web = QWebEngineView()
#         self.channel = QWebChannel()
#         self.bridge = Bridge()
#         self.bridge.parent_window = self
#         self.channel.registerObject("pyBridge", self.bridge)
#         self.web.page().setWebChannel(self.channel)
#         self.inject_webchannel_js()

#         first_level = "Level 1 (500 words)"
#         self.web.load(QUrl(f"{self.BASE_URL}-1-1"))
#         self.web.loadFinished.connect(self.inject_button_script)

#         # --- Dashboard labels ---
#         self.statuses = ["Not Seen", "Want to Know", "Known"]
#         self.anki_states = ["Want to Add", "In Anki", "Will Not Add"]
#         self.status_labels = {}
#         self.anki_labels = {}
#         self.combo_labels = {}

#         # Individual status labels
#         for status, color in [("Not Seen", "lightgray"), ("Want to Know", "lightyellow"), ("Known", "lightgreen")]:
#             lbl = QLabel(f"{status}: 0")
#             lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
#             lbl.setStyleSheet(f"font-weight:bold; background-color:{color}; padding:3px; border:1px solid gray;")
#             self.status_labels[status] = lbl

#         # Anki labels
#         anki_colors = {
#             "Want to Add": "lightblue",
#             "In Anki": "lightgreen",
#             "Will Not Add": "#f08080"  # red
#         }
#         for a in self.anki_states:
#             lbl = QLabel(f"{a}: 0")
#             lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
#             lbl.setStyleSheet(f"font-weight:bold; background-color:{anki_colors[a]}; padding:3px; border:1px solid gray;")
#             self.anki_labels[a] = lbl

#         # Combo labels (friendly names)
#         combo_name_map = {
#             "Want to Know + Want to Add": "Brand New",
#             "Want to Know + In Anki": "Learning",
#             "Known + Want to Add": "Familiar",
#             "Known + In Anki": "Learned",
#         }
#         combo_colors = {
#             "Brand New": "#fff5b1",
#             "Learning": "#b3e0ff",
#             "Familiar": "#d4f8d4",
#             "Learned": "#a0f0a0",
#         }
#         for raw_key, name in combo_name_map.items():
#             lbl = QLabel(f"{name}: 0")
#             lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
#             lbl.setStyleSheet(f"font-weight:bold; background-color:{combo_colors[name]}; padding:3px; border:1px solid gray;")
#             self.combo_labels[raw_key] = lbl

#         # Level & page dropdowns
#         self.level_dropdown = QComboBox()
#         self.level_dropdown.addItems([f"Level {lvl} ({cfg['words']} words)" for lvl, cfg in self.LEVEL_CONFIG.items()])
#         self.level_dropdown.currentTextChanged.connect(self.on_level_changed)
#         self.page_dropdown = QComboBox()
#         self.page_dropdown.currentTextChanged.connect(self.on_page_changed)
#         self.update_page_dropdown(first_level)

#         # Dashboard layout
#         dashboard_layout = QVBoxLayout()
#         dashboard_layout.addWidget(QLabel("Level:"))
#         dashboard_layout.addWidget(self.level_dropdown)
#         dashboard_layout.addWidget(QLabel("Page:"))
#         dashboard_layout.addWidget(self.page_dropdown)

#         # Add all labels
#         for lbl in self.status_labels.values():
#             dashboard_layout.addWidget(lbl)
#         for lbl in self.anki_labels.values():
#             dashboard_layout.addWidget(lbl)
#         for lbl in self.combo_labels.values():
#             dashboard_layout.addWidget(lbl)

#         dashboard_layout.addStretch()

#         # Main layout
#         main_layout = QHBoxLayout(self)
#         main_layout.addLayout(dashboard_layout, 0)
#         main_layout.addWidget(self.web, 1)

#         # Connect callback
#         self.bridge.status_changed_callback = self.update_dashboard
#         self.update_dashboard()

#     def update_dashboard(self):
#         # Initialize counters
#         status_counts = {s: 0 for s in self.statuses}
#         anki_counts = {a: 0 for a in self.anki_states}
#         combo_counts = {
#             "Want to Know + Want to Add": 0,
#             "Want to Know + In Anki": 0,
#             "Known + Want to Add": 0,
#             "Known + In Anki": 0,
#         }

#         # Count saved words
#         for e in self.bridge.data:
#             status = e.get("status", "Not Seen")
#             anki = e.get("anki", "Want to Add")

#             # Count statuses
#             if status in status_counts:
#                 status_counts[status] += 1

#             # Count Anki states
#             if status != "Not Seen" and anki in anki_counts:
#                 anki_counts[anki] += 1

#             # Count combos (normal ones only)
#             key = f"{status} + {anki}"
#             if key in combo_counts:
#                 combo_counts[key] += 1

#         # JS to count Not Seen buttons that haven't been saved yet
#         js_not_seen = """
#             Array.from(document.querySelectorAll('.status-btn'))
#                 .filter(btn => btn.textContent.trim() === 'Not Seen')
#                 .length;
#         """

#         def handle_not_seen(not_seen_count):
#             # Update status labels
#             for s, lbl in self.status_labels.items():
#                 if s == "Not Seen":
#                     lbl.setText(f"{s}: {status_counts[s] + not_seen_count}")
#                 else:
#                     lbl.setText(f"{s}: {status_counts[s]}")

#             # Update Anki labels (includes Will Not Add)
#             for a, lbl in self.anki_labels.items():
#                 lbl.setText(f"{a}: {anki_counts.get(a, 0)}")

#             # Update combo labels with friendly names
#             combo_name_map = {
#                 "Want to Know + Want to Add": "Brand New",
#                 "Want to Know + In Anki": "Learning",
#                 "Known + Want to Add": "Familiar",
#                 "Known + In Anki": "Learned",
#             }
#             for raw_key, lbl in self.combo_labels.items():
#                 friendly_name = combo_name_map[raw_key]
#                 lbl.setText(f"{friendly_name}: {combo_counts.get(raw_key, 0)}")

#         self.web.page().runJavaScript(js_not_seen, handle_not_seen)



#     def update_page_dropdown(self, level_name):
#         """Generate page ranges and URLs for the dropdown based on level"""
#         self.page_dropdown.blockSignals(True)
#         self.page_dropdown.clear()

#         # Extract level number from text
#         level_num = int(level_name.split()[1])
#         config = self.LEVEL_CONFIG[level_num]
#         step = config["step"]
#         total_words = config["words"]

#         ranges = []
#         urls = []

#         # First page always ends with -1
#         ranges.append(f"1-{min(step, total_words)}")
#         urls.append(f"{self.BASE_URL}-{level_num}-1")

#         # Subsequent pages
#         for start in range(1 + step, total_words + 1, step):
#             end = min(start + step - 1, total_words)
#             ranges.append(f"{start}-{end}")
#             urls.append(f"{self.BASE_URL}-{level_num}-{start}")

#         # Populate dropdown
#         for range_label, url in zip(ranges, urls):
#             self.page_dropdown.addItem(range_label, url)

#         self.page_dropdown.setCurrentIndex(0)
#         self.page_dropdown.blockSignals(False)

#     def on_level_changed(self, level_name):
#         self.update_page_dropdown(level_name)
#         # Load first page of the selected level
#         first_url = self.page_dropdown.itemData(0)
#         if first_url:
#             self.web.load(QUrl(first_url))

#     def on_page_changed(self, _):
#         url = self.page_dropdown.currentData()
#         if url:
#             self.web.load(QUrl(url))


#     def inject_webchannel_js(self):
#         script = QWebEngineScript()
#         script.setName("qwebchannel_loader")
#         script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
#         script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
#         script.setRunsOnSubFrames(False)
#         script.setSourceCode("""
#             var s = document.createElement("script");
#             s.src = "qrc:///qtwebchannel/qwebchannel.js";
#             document.documentElement.appendChild(s);
#         """)
#         self.web.page().profile().scripts().insert(script)

#     def inject_button_script(self):
#         script = r"""
#             function loadQWebChannelAndButtons() {
#                 if (!document.body) {
#                     setTimeout(loadQWebChannelAndButtons, 100);
#                     return;
#                 }

#                 if (typeof QWebChannel === 'undefined') {
#                     if (!document.getElementById('qwebchannel-js')) {
#                         var s = document.createElement('script');
#                         s.id = 'qwebchannel-js';
#                         s.src = 'qrc:///qtwebchannel/qwebchannel.js';
#                         s.onload = loadQWebChannelAndButtons;
#                         document.head.appendChild(s);
#                     }
#                     return;
#                 }

#                 new QWebChannel(qt.webChannelTransport, function(channel) {
#                     const py = channel.objects.pyBridge;

#                     function processRows() {
#                         const rows = document.querySelectorAll(".jukugorow");
#                         if (!rows.length) { setTimeout(processRows, 200); return; }

#                         py.getSavedWords(function(savedStr) {
#                             const savedWords = JSON.parse(savedStr);

#                             rows.forEach(block => {
#                                 const anchor = block.querySelector("a");
#                                 if (!anchor || block.querySelector('.status-btn')) return;

#                                 let word = "", furigana = "";
#                                 anchor.childNodes.forEach(node => {
#                                     if (node.nodeType === Node.ELEMENT_NODE && node.classList.contains("f_container")) {
#                                         word += node.querySelector(".f_kanji")?.innerText || "";
#                                         furigana += node.querySelector(".furigana")?.innerText || "";
#                                     } else if (node.nodeType === Node.TEXT_NODE) {
#                                         word += node.textContent;
#                                         furigana += node.textContent;
#                                     }
#                                 });
#                                 word = word.trim() || furigana.trim();
#                                 furigana = furigana.trim();

#                                 const entryObj = {
#                                     word: word,
#                                     furigana: furigana,
#                                     jlpt: block.querySelector(".jlpt_container span")?.className.match(/ja-jlpt_(\d+)/)?.[1] ? "N" + block.querySelector(".jlpt_container span").className.match(/ja-jlpt_(\d+)/)[1] : "",
#                                     usefulness: block.querySelector(".ufn_container span")?.className.match(/ja-ufn_(\d+)/)?.[1] ? parseInt(block.querySelector(".ufn_container span").className.match(/ja-ufn_(\d+)/)[1]) : 0,
#                                     anki: "Will Not Add"
#                                 };

#                                 const savedEntry = savedWords.find(e => e.word === entryObj.word && e.furigana === entryObj.furigana);
#                                 let currentStatus = savedEntry?.status || "Not Seen";
#                                 let currentAnki = savedEntry?.anki || "Want to Add";

#                                 // --- Main Status Button ---
#                                 const btn = document.createElement("button");
#                                 btn.className = "status-btn";
#                                 btn.style.marginLeft = "5px";
#                                 btn.style.padding = "2px 6px";

#                                 // --- Single Anki Button (cycles through 3 states) ---
#                                 const ankiBtn = document.createElement("button");
#                                 ankiBtn.className = "anki-btn";
#                                 ankiBtn.style.marginLeft = "5px";
#                                 ankiBtn.style.padding = "2px 6px";

#                                 const statusStates = ["Not Seen", "Want to Know", "Known"];
#                                 const ankiStates = ["Will Not Add", "Want to Add", "In Anki"];

#                                 function updateRowColor() {
#                                     if (currentStatus === "Not Seen") {
#                                         block.style.backgroundColor = "#f0f0f0"; // Not Seen gray
#                                     } else if (currentStatus === "Known" && currentAnki === "In Anki") {
#                                         block.style.backgroundColor = "#a0f0a0"; // Learned
#                                     } else if (currentStatus === "Known" && currentAnki === "Want to Add") {
#                                         block.style.backgroundColor = "#d4f8d4"; // Familiar
#                                     } else if (currentStatus === "Want to Know" && currentAnki === "In Anki") {
#                                         block.style.backgroundColor = "#b3e0ff"; // Learning
#                                     } else if (currentStatus === "Want to Know" && currentAnki === "Want to Add") {
#                                         block.style.backgroundColor = "#fff5b1"; // Brand New
#                                     } else if (currentAnki === "Will Not Add") {
#                                         block.style.backgroundColor = "#f08080"; // Will Not Add = red
#                                     } else {
#                                         block.style.backgroundColor = "#f0f0f0"; // fallback
#                                     }
#                                 }


#                                 function updateAnkiButton() {
#                                     if (currentStatus === "Not Seen") {
#                                         ankiBtn.disabled = true;
#                                         ankiBtn.textContent = "";
#                                         ankiBtn.style.backgroundColor = "lightgray";
#                                     } else {
#                                         ankiBtn.disabled = false;
#                                         ankiBtn.textContent = currentAnki;
#                                         ankiBtn.style.backgroundColor = currentAnki === "In Anki" ? "#a0d8f0" :
#                                                                     currentAnki === "Want to Add" ? "lightgray" :
#                                                                     "#f08080"; // Will Not Add
#                                     }
#                                     updateRowColor();
#                                 }

#                                 function updateStatusButton() {
#                                     btn.textContent = currentStatus;
#                                     btn.style.backgroundColor = currentStatus === "Known" ? "lightgreen" :
#                                                             currentStatus === "Want to Know" ? "lightyellow" : "";
#                                     updateAnkiButton();
#                                 }

#                                 btn.onclick = () => {
#                                     const idx = statusStates.indexOf(currentStatus);
#                                     currentStatus = statusStates[(idx + 1) % statusStates.length];
#                                     updateStatusButton();
#                                     py.setWordStatus(JSON.stringify({...entryObj, anki: currentAnki}), currentStatus);
#                                 };

#                                 ankiBtn.onclick = () => {
#                                     if (currentStatus === "Not Seen") return;
#                                     const idx = ankiStates.indexOf(currentAnki);
#                                     currentAnki = ankiStates[(idx + 1) % ankiStates.length];
#                                     updateAnkiButton();
#                                     py.setWordStatus(JSON.stringify({...entryObj, anki: currentAnki}), currentStatus);
#                                 };

#                                 updateStatusButton();
#                                 block.appendChild(btn);
#                                 block.appendChild(ankiBtn);
#                             });

#                             if (py.updateNotSeenDashboard) py.updateNotSeenDashboard();
#                         });
#                     }

#                     processRows();
#                 });
#             }

#             if (document.readyState === "loading") {
#                 document.addEventListener("DOMContentLoaded", loadQWebChannelAndButtons);
#             } else {
#                 loadQWebChannelAndButtons();
#             }
#         """
#         self.web.page().runJavaScript(script)



# if __name__ == "__main__":
#     app = QApplication(['pyqt'])
#     w = Window()
#     w.resize(1400, 900)
#     w.show()
#     app.exec()












"""
Everything works just added in dashboard counters for 
N0,N5 - N1
And usefulness of 1-5
"""
import json
import os
from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineScript
from PyQt6.QtWebChannel import QWebChannel

JSON_FILE = "words.json"


class Bridge(QObject):
    def __init__(self):
        super().__init__()
        self.data = []
        self.status_changed_callback = None
        self.parent_window = None
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                self.data = json.load(f)

    @pyqtSlot(result=str)
    def getSavedWords(self):
        return json.dumps(self.data)

    @pyqtSlot(str, str)
    def setWordStatus(self, json_data, status):
        entry = json.loads(json_data)
        # Remove existing entry
        self.data = [e for e in self.data if not (e.get("word") == entry.get("word") and e.get("furigana") == entry.get("furigana"))]
        # Add if status is not "Not Seen"
        if status != "Not Seen":
            entry["status"] = status
            self.data.append(entry)
        self._write_json()
        # Trigger dashboard update
        if self.status_changed_callback:
            self.status_changed_callback()

    @pyqtSlot()
    def updateNotSeenDashboard(self):
        if self.parent_window:
            self.parent_window.update_dashboard()

    def _write_json(self):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)


class Window(QWidget):
    LEVEL_CONFIG = {
        1: {"words": 500, "step": 100},
        2: {"words": 1000, "step": 100},
        3: {"words": 1500, "step": 100},
        4: {"words": 2000, "step": 100},
        5: {"words": 5000, "step": 100},
    }

    BASE_URL = "https://www.kanshudo.com/collections/vocab_usefulness2021/UFN2021"

    def __init__(self):
        super().__init__()

        # --- WebEngine setup ---
        self.web = QWebEngineView()
        self.channel = QWebChannel()
        self.bridge = Bridge()
        self.bridge.parent_window = self
        self.channel.registerObject("pyBridge", self.bridge)
        self.web.page().setWebChannel(self.channel)
        self.inject_webchannel_js()

        first_level = "Level 1 (500 words)"
        self.web.load(QUrl(f"{self.BASE_URL}-1-1"))
        self.web.loadFinished.connect(self.inject_button_script)

        # --- Labels ---
        self.statuses = ["Not Seen", "Want to Know", "Known"]
        self.anki_states = ["Want to Add", "In Anki", "Will Not Add"]
        self.jlpt_levels = ["N1", "N2", "N3", "N4", "N5", "N0"]
        self.usefulness_levels = [1, 2, 3, 4, 5]

        self.status_labels = {}
        self.anki_labels = {}
        self.combo_labels = {}
        self.jlpt_labels = {}
        self.usefulness_labels = {}

        # Status labels
        for status, color in [("Not Seen", "lightgray"), ("Want to Know", "lightyellow"), ("Known", "lightgreen")]:
            lbl = QLabel(f"{status}: 0")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(f"font-weight:bold; background-color:{color}; padding:3px; border:1px solid gray;")
            self.status_labels[status] = lbl

        # Anki labels
        anki_colors = {"Want to Add": "lightblue", "In Anki": "lightgreen", "Will Not Add": "#f08080"}
        for a in self.anki_states:
            lbl = QLabel(f"{a}: 0")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(f"font-weight:bold; background-color:{anki_colors[a]}; padding:3px; border:1px solid gray;")
            self.anki_labels[a] = lbl

        # Combo labels
        combo_name_map = {
            "Want to Know + Want to Add": "Brand New",
            "Want to Know + In Anki": "Learning",
            "Known + Want to Add": "Familiar",
            "Known + In Anki": "Learned",
        }
        combo_colors = {"Brand New": "#fff5b1", "Learning": "#b3e0ff", "Familiar": "#d4f8d4", "Learned": "#a0f0a0"}
        for raw_key, name in combo_name_map.items():
            lbl = QLabel(f"{name}: 0")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(f"font-weight:bold; background-color:{combo_colors[name]}; padding:3px; border:1px solid gray;")
            self.combo_labels[raw_key] = lbl

        # JLPT labels (vertical)
        for lvl in self.jlpt_levels:
            lbl = QLabel(f"{lvl}: 0")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("font-weight:bold; background-color:#e0e0e0; padding:3px; border:1px solid gray;")
            self.jlpt_labels[lvl] = lbl

        # Usefulness labels (vertical)
        for u in self.usefulness_levels:
            lbl = QLabel(f"Usefulness {u}: 0")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("font-weight:bold; background-color:#f0f0f0; padding:3px; border:1px solid gray;")
            self.usefulness_labels[u] = lbl

        # --- Level & Page dropdowns ---
        self.level_dropdown = QComboBox()
        self.level_dropdown.addItems([f"Level {lvl} ({cfg['words']} words)" for lvl, cfg in self.LEVEL_CONFIG.items()])
        self.level_dropdown.currentTextChanged.connect(self.on_level_changed)
        self.page_dropdown = QComboBox()
        self.page_dropdown.currentTextChanged.connect(self.on_page_changed)
        self.update_page_dropdown(first_level)

        # --- Dashboard layout (vertical) ---
        dashboard_layout = QVBoxLayout()
        dashboard_layout.addWidget(QLabel("Level:"))
        dashboard_layout.addWidget(self.level_dropdown)
        dashboard_layout.addWidget(QLabel("Page:"))
        dashboard_layout.addWidget(self.page_dropdown)

        # Add all labels vertically
        for lbl in self.status_labels.values(): dashboard_layout.addWidget(lbl)
        for lbl in self.anki_labels.values(): dashboard_layout.addWidget(lbl)
        for lbl in self.combo_labels.values(): dashboard_layout.addWidget(lbl)
        for lbl in self.jlpt_labels.values(): dashboard_layout.addWidget(lbl)
        for lbl in self.usefulness_labels.values(): dashboard_layout.addWidget(lbl)

        dashboard_layout.addStretch()

        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.addLayout(dashboard_layout, 0)
        main_layout.addWidget(self.web, 1)

        # Connect callback
        self.bridge.status_changed_callback = self.update_dashboard
        self.update_dashboard()

    def update_dashboard(self):
        # Initialize counters
        status_counts = {s: 0 for s in self.statuses}
        anki_counts = {a: 0 for a in self.anki_states}
        combo_counts = {
            "Want to Know + Want to Add": 0,
            "Want to Know + In Anki": 0,
            "Known + Want to Add": 0,
            "Known + In Anki": 0,
        }
        jlpt_counts = {lvl: 0 for lvl in self.jlpt_levels}
        usefulness_counts = {u: 0 for u in self.usefulness_levels}

        # Count saved words
        for e in self.bridge.data:
            status = e.get("status", "Not Seen")
            anki = e.get("anki", "Want to Add")
            jlpt = e.get("jlpt")
            usefulness = e.get("usefulness")

            # Status
            if status in status_counts: status_counts[status] += 1
            if status != "Not Seen" and anki in anki_counts: anki_counts[anki] += 1

            # Combo
            key = f"{status} + {anki}"
            if key in combo_counts: combo_counts[key] += 1

            # JLPT
            if jlpt in jlpt_counts: jlpt_counts[jlpt] += 1

            # Usefulness
            if usefulness in usefulness_counts: usefulness_counts[usefulness] += 1

        # JS for not seen buttons
        js_not_seen = """
            Array.from(document.querySelectorAll('.status-btn'))
                .filter(btn => btn.textContent.trim() === 'Not Seen')
                .length;
        """

        def handle_not_seen(not_seen_count):
            # Update statuses
            for s, lbl in self.status_labels.items():
                lbl.setText(f"{s}: {status_counts[s] + (not_seen_count if s=='Not Seen' else 0)}")

            # Update Anki
            for a, lbl in self.anki_labels.items():
                lbl.setText(f"{a}: {anki_counts.get(a, 0)}")

            # Update combo
            combo_name_map = {
                "Want to Know + Want to Add": "Brand New",
                "Want to Know + In Anki": "Learning",
                "Known + Want to Add": "Familiar",
                "Known + In Anki": "Learned",
            }
            for raw_key, lbl in self.combo_labels.items():
                friendly_name = combo_name_map[raw_key]
                lbl.setText(f"{friendly_name}: {combo_counts.get(raw_key, 0)}")

            # Update JLPT & Usefulness
            for lvl, lbl in self.jlpt_labels.items():
                lbl.setText(f"{lvl}: {jlpt_counts.get(lvl, 0)}")
            for u, lbl in self.usefulness_labels.items():
                lbl.setText(f"Usefulness {u}: {usefulness_counts.get(u, 0)}")

        self.web.page().runJavaScript(js_not_seen, handle_not_seen)

    # --- Page / Level dropdowns ---
    def update_page_dropdown(self, level_name):
        self.page_dropdown.blockSignals(True)
        self.page_dropdown.clear()
        level_num = int(level_name.split()[1])
        cfg = self.LEVEL_CONFIG[level_num]
        step, total = cfg["step"], cfg["words"]

        ranges, urls = [], []
        ranges.append(f"1-{min(step, total)}")
        urls.append(f"{self.BASE_URL}-{level_num}-1")
        for start in range(1 + step, total + 1, step):
            end = min(start + step - 1, total)
            ranges.append(f"{start}-{end}")
            urls.append(f"{self.BASE_URL}-{level_num}-{start}")

        for r, u in zip(ranges, urls):
            self.page_dropdown.addItem(r, u)
        self.page_dropdown.setCurrentIndex(0)
        self.page_dropdown.blockSignals(False)

    def on_level_changed(self, level_name):
        self.update_page_dropdown(level_name)
        url = self.page_dropdown.itemData(0)
        if url: self.web.load(QUrl(url))

    def on_page_changed(self, _):
        url = self.page_dropdown.currentData()
        if url: self.web.load(QUrl(url))

    # --- WebChannel JS ---
    def inject_webchannel_js(self):
        script = QWebEngineScript()
        script.setName("qwebchannel_loader")
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
        script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        script.setRunsOnSubFrames(False)
        script.setSourceCode("""
            var s = document.createElement("script");
            s.src = "qrc:///qtwebchannel/qwebchannel.js";
            document.documentElement.appendChild(s);
        """)
        self.web.page().profile().scripts().insert(script)

    def inject_button_script(self):
        script = r"""
            function loadQWebChannelAndButtons() {
                if (!document.body) {
                    setTimeout(loadQWebChannelAndButtons, 100);
                    return;
                }

                if (typeof QWebChannel === 'undefined') {
                    if (!document.getElementById('qwebchannel-js')) {
                        var s = document.createElement('script');
                        s.id = 'qwebchannel-js';
                        s.src = 'qrc:///qtwebchannel/qwebchannel.js';
                        s.onload = loadQWebChannelAndButtons;
                        document.head.appendChild(s);
                    }
                    return;
                }

                new QWebChannel(qt.webChannelTransport, function(channel) {
                    const py = channel.objects.pyBridge;

                    function processRows() {
                        const rows = document.querySelectorAll(".jukugorow");
                        if (!rows.length) { setTimeout(processRows, 200); return; }

                        py.getSavedWords(function(savedStr) {
                            const savedWords = JSON.parse(savedStr);

                            rows.forEach(block => {
                                const anchor = block.querySelector("a");
                                if (!anchor || block.querySelector('.status-btn')) return;

                                let word = "", furigana = "";
                                anchor.childNodes.forEach(node => {
                                    if (node.nodeType === Node.ELEMENT_NODE && node.classList.contains("f_container")) {
                                        word += node.querySelector(".f_kanji")?.innerText || "";
                                        furigana += node.querySelector(".furigana")?.innerText || "";
                                    } else if (node.nodeType === Node.TEXT_NODE) {
                                        word += node.textContent;
                                        furigana += node.textContent;
                                    }
                                });
                                word = word.trim() || furigana.trim();
                                furigana = furigana.trim();

                                const entryObj = {
                                    word: word,
                                    furigana: furigana,
                                    jlpt: block.querySelector(".jlpt_container span")?.className.match(/ja-jlpt_(\d+)/)?.[1] ? "N" + block.querySelector(".jlpt_container span").className.match(/ja-jlpt_(\d+)/)[1] : "",
                                    usefulness: block.querySelector(".ufn_container span")?.className.match(/ja-ufn_(\d+)/)?.[1] ? parseInt(block.querySelector(".ufn_container span").className.match(/ja-ufn_(\d+)/)[1]) : 0,
                                    anki: "Will Not Add"
                                };

                                const savedEntry = savedWords.find(e => e.word === entryObj.word && e.furigana === entryObj.furigana);
                                let currentStatus = savedEntry?.status || "Not Seen";
                                let currentAnki = savedEntry?.anki || "Want to Add";

                                // --- Main Status Button ---
                                const btn = document.createElement("button");
                                btn.className = "status-btn";
                                btn.style.marginLeft = "5px";
                                btn.style.padding = "2px 6px";

                                // --- Single Anki Button (cycles through 3 states) ---
                                const ankiBtn = document.createElement("button");
                                ankiBtn.className = "anki-btn";
                                ankiBtn.style.marginLeft = "5px";
                                ankiBtn.style.padding = "2px 6px";

                                const statusStates = ["Not Seen", "Want to Know", "Known"];
                                const ankiStates = ["Will Not Add", "Want to Add", "In Anki"];

                                function updateRowColor() {
                                    if (currentStatus === "Not Seen") {
                                        block.style.backgroundColor = "#f0f0f0"; // Not Seen gray
                                    } else if (currentStatus === "Known" && currentAnki === "In Anki") {
                                        block.style.backgroundColor = "#a0f0a0"; // Learned
                                    } else if (currentStatus === "Known" && currentAnki === "Want to Add") {
                                        block.style.backgroundColor = "#d4f8d4"; // Familiar
                                    } else if (currentStatus === "Want to Know" && currentAnki === "In Anki") {
                                        block.style.backgroundColor = "#b3e0ff"; // Learning
                                    } else if (currentStatus === "Want to Know" && currentAnki === "Want to Add") {
                                        block.style.backgroundColor = "#fff5b1"; // Brand New
                                    } else if (currentAnki === "Will Not Add") {
                                        block.style.backgroundColor = "#f08080"; // Will Not Add = red
                                    } else {
                                        block.style.backgroundColor = "#f0f0f0"; // fallback
                                    }
                                }


                                function updateAnkiButton() {
                                    if (currentStatus === "Not Seen") {
                                        ankiBtn.disabled = true;
                                        ankiBtn.textContent = "";
                                        ankiBtn.style.backgroundColor = "lightgray";
                                    } else {
                                        ankiBtn.disabled = false;
                                        ankiBtn.textContent = currentAnki;
                                        ankiBtn.style.backgroundColor = currentAnki === "In Anki" ? "#a0d8f0" :
                                                                    currentAnki === "Want to Add" ? "lightgray" :
                                                                    "#f08080"; // Will Not Add
                                    }
                                    updateRowColor();
                                }

                                function updateStatusButton() {
                                    btn.textContent = currentStatus;
                                    btn.style.backgroundColor = currentStatus === "Known" ? "lightgreen" :
                                                            currentStatus === "Want to Know" ? "lightyellow" : "";
                                    updateAnkiButton();
                                }

                                btn.onclick = () => {
                                    const idx = statusStates.indexOf(currentStatus);
                                    currentStatus = statusStates[(idx + 1) % statusStates.length];
                                    updateStatusButton();
                                    py.setWordStatus(JSON.stringify({...entryObj, anki: currentAnki}), currentStatus);
                                };

                                ankiBtn.onclick = () => {
                                    if (currentStatus === "Not Seen") return;
                                    const idx = ankiStates.indexOf(currentAnki);
                                    currentAnki = ankiStates[(idx + 1) % ankiStates.length];
                                    updateAnkiButton();
                                    py.setWordStatus(JSON.stringify({...entryObj, anki: currentAnki}), currentStatus);
                                };

                                updateStatusButton();
                                block.appendChild(btn);
                                block.appendChild(ankiBtn);
                            });

                            if (py.updateNotSeenDashboard) py.updateNotSeenDashboard();
                        });
                    }

                    processRows();
                });
            }

            if (document.readyState === "loading") {
                document.addEventListener("DOMContentLoaded", loadQWebChannelAndButtons);
            } else {
                loadQWebChannelAndButtons();
            }
        """
        self.web.page().runJavaScript(script)



if __name__ == "__main__":
    app = QApplication(['pyqt'])
    w = Window()
    w.resize(1400, 900)
    w.show()
    app.exec()
