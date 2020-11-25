# RSA-Implementation

A implementation of RSA for my SOP

This implementation should not be seen as secure in anyway.

## Installation

Install [python3](https://python.org/downloads/)

Download and unzip the primenumber list from [here](https://lyngbyekolbe.dk/RSA_Implementation/primenums.zip) in the root of the project

## Usage

Run **keygen.py** to generate your keypair:

```bash
python keygen.py -b <keysize>
```

You will get two files in the **generated_keys** directory. The files is named in the format

```text
<year>-<month>-<day>_<hours><minutes><seconds>.<priv|pub>.json
```

The first extension declares if the key is private or public. You can share the public with others, but keep the private secret.