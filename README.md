# Ders\_Control

**Ders\_Control** is a schedule-making tool designed specifically for **Kadir Has University's SPARKS system**. It allows you to scrape your classes from SPARKS into a JSON format and easily filter and organize them into a personalized class schedule.

---

## Features

* Scrape classes from SPARKS into JSON files.
* Filter and arrange classes into your own schedule.
* View class placement visually in a calendar format.
* Customize class colors and manage your schedule interactively.
* Works entirely in your browser with local storage (no backend required).

---

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/OzanKutlar/Ders_Control.git
cd Ders_Control
```

---

### Step 1: Scrape Your Classes

You can scrape SPARKS in **two ways**:

#### 1. Manual Method

1. Open `browserInject.js` and copy its contents.
2. Navigate to the SPARKS page with your desired classes.
3. Press `F12` or right-click → **Inspect** to open Developer Tools.
4. Paste the code into the browser's console.
5. A pop-up will appear asking you to name the JSON file. For example, name it `Engineering`.
6. A file named `Engineering.json` will be downloaded to your **Downloads** folder.

#### 2. Bookmark Method (Recommended)

1. Run `converter.py` to convert `browserInject.js` into a bookmarklet.
2. Save the bookmarklet as a bookmark.
3. Navigate to the SPARKS page where your classes are displayed.
4. Press the bookmarklet.
5. A pop-up will appear asking you to name the JSON file. For example, `Engineering`.
6. The JSON file will be downloaded to your **Downloads** folder.

> 📌 Not familiar with bookmarklets? Learn more [here](https://en.wikipedia.org/wiki/Bookmarklet).

---

### Step 2: Load Your Schedule

1. Run the Python server:

```bash
python server.py
```

This will start a local HTTP server.

2. Open `index.html` in your browser.

3. Press **Load Schedule JSON**. The server will scan your **Downloads** folder for JSON files.

4. Select the JSON file you downloaded. Your class list will appear on the right.

---

### Step 3: Organize Your Schedule

* Click on any class to see its placement in the schedule.
* Press the small **checkmark** below to permanently add it to your schedule.
* Clicking a class inside the schedule allows you to:

  * Change its color
  * Remove it from the schedule

> All schedule data is stored locally in the browser’s **IndexedDB**. Currently, **export or import of schedules is not supported**.

---

## Requirements

* Python 3.x
* Modern web browser (Chrome, Firefox, Edge, etc.)

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for new features, bug fixes, or improvements.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

Made with ❤️ for Kadir Has University students by Kadir Has University students.