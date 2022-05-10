# rev1

Parse [MCNP](https://mcnp.lanl.gov) Rev-1 file

## Environment

Python 3.10 or later

## Usage

Download `rev1.py` manually, and put it on your working directory.

```python
import rev1

# parsing a Rev-1 file
with open("REV1.01v") as f:
    parsed: Rev1 = rev1.load(f)

print(parsed.info)
```

`Rev1` class is composed with `Nxs`, `Jxs`, and `Xss` class.

The classes and their member variables are based on [Covariance Data File Formats for Whisper-1.0 & Whisper-1.1](https://mcnp.lanl.gov/pdf_files/la-ur-17-20098.pdf). Please refer to it.

## Note

- `zaid.py` can encode general zaids into internal expressions of Rev-1, and vice versa.

- `example.py` shows an example of parsing a Rev-1 file.
