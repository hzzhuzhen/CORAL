## Environment Configuration

Create a virtual environment:

```shell
conda create -n freeal python=3.11
conda activate freeal
```

Install related packages:

```
pip install -r requirements.txt
```

## Run

Start by:

```
python app.py
```

Start with debug by:

```
python -m debugpy --listen localhost:5678 --wait-for-client app.py
```

## APIs

| Method | Route           | Description                 |
| ------ | --------------- | --------------------------- |
| [POST] | `/llm`          | Upload user data.           |
| [GET]  | `/llm`          | Initial labeling with LLM.  |
| [GET]  | `/llm/refinery` | Refinery labeling with LLM. |
| [GET]  | `/slm`          | Distilling with SLM.        |
| [GET]  | `/slm/refinery` | Refinery labeling with SLM. |
| [POST] | `/manual`       | Manual correction.          |