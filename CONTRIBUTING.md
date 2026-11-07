# 🤝 Contributing to Mini Embedding Explorer

Thank you for your interest in contributing.

Mini Embedding Explorer is designed to stay lightweight, easy to understand, and accessible to both developers and non-technical users. Contributions that improve usability, reliability, testing, performance, and documentation are especially welcome.

---

## 🏭 Getting Started

### Clone the Repository

```bash
git clone https://github.com/reory/mini_embedding_explorer.git
cd mini_embedding_explorer
```

### Install Dependencies

```bash
uv sync
```

### Run the Application

```bash
streamlit run app.py
```

### Run the Test Suite

```bash
uv run -m pytest
```

---

## 🧩 Contribution Guidelines

Please keep contributions:

- Small and focused
- Well documented
- Consistent with the existing code style
- Backed by tests where practical

### ✅ Good Contributions

- Bug fixes
- New tests
- Documentation improvements
- Performance improvements
- User experience enhancements
- Roadmap features

### ❌ Please Avoid

- Large unrelated changes in a single pull request
- Unnecessary dependencies
- Major refactors without discussion
- Breaking existing functionality

---

## 🧪 Testing

Before opening a pull request, please ensure:

```bash
uv run -m pytest
```

runs successfully.

New features should include tests where appropriate.

---

## 📄 Expected Data Formats

### CSV Files

Mini Embedding Explorer works best with datasets containing one text record per row.

Example:

```csv
feedback
"Delivery arrived two days late and the tracking link never updated"
"The mobile app keeps crashing whenever I try to upload receipts"
"Customer service was extremely helpful resolving my billing issue"
```

### TXT Files

TXT files should contain one text record per line.

Example:

```text
Delivery arrived two days late and the tracking link never updated
The mobile app keeps crashing whenever I try to upload receipts
Customer service was extremely helpful resolving my billing issue
```

---

## 🛣️ Roadmap Areas

Contributions are especially welcome in:

- Interactive Cluster Visualisation
- Lightweight NLP Mode
- Advanced Embedding Models
- Smart CSV Import
- Interactive Cluster Editing
- Semantic Search Engine

---

## 📸 UI Changes

If your contribution changes the user interface, please include screenshots in your pull request.

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.
