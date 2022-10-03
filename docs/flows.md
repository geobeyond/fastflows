# Flows

### Run flow with Parameters

#### With command line

```console

    fastflows flows run file_reader --params "{'path_to_file': 'test.txt'}"

```

#### With REST API

```python
    # arguments that expected by your flow

    params = {'path_to_file': 'test.txt'}

    # where file_reader - flow_name
    response = client.post(f"/flows/name/file_reader",
        json={"parameters": params})

```
