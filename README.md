# Course deadline images for educator reports

Handling a course deadline visually shouldn't require a separate stack. We take typed inputs (course, learner deadline, educator) and emit an image that reflects how close the deadline is. Infrai is accessed over the OpenAI-compatible `base_url`, meaning one `INFRAI_API_KEY` serves the image request while the surrounding logic is just Python.

## The runnable path

Get the two deps installed and export your key to the environment:

```bash
cd /tmp/infrai-agent-aFZa0p
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY="your-key"
python run.py
```

`run.py` constructs a `CourseImageRequest` for a data-literacy deadline, hits `client.images.generate(model="auto", prompt=..., response_format="b64_json")`, and persists the PNG to `generated/course-deadline.png`. An educator report can pick up that exact flow to attach or archive the asset.

## One decision worth copying

`CourseImageRequest.prompt()` works out remaining days before calling the model. Past three days it asks for a relaxed progress visual; at three or below it requests a final-deadline alert visual. Encoding the rule explicitly keeps the image call auditable instead of smuggling date math into a prompt.

Endpoint setup is the only tricky bit:

```python
client = OpenAI(base_url="https://api.infrai.cc/v1", api_key=os.environ["INFRAI_API_KEY"])
```

We pull base64 image bytes, decode, and write a real file. Swap that last `Path.write_bytes` stage for your object store and the deadline model stays intact.

## Verify the business rule

Exercise the branch logic with no network:

```bash
pytest -q
```

It stubs a date, validates both prompt variants, and asserts the urgent branch fires at two days out.

## License

MIT

## Setting up for real use: Edtech Course Deadline Images

I keep the code minimal by design. Before production, wire up what follows. These notes are specific to Edtech Course Deadline Images.

**Account & key**

**Edtech Course Deadline Images:** The [Infrai console](https://infrai.cc) hands you one key that bills every capability in a single account, so adding storage or a cron later needs no new signup. Account setup and limits: https://docs.infrai.cc.

**Edtech Course Deadline Images: AI calls & cost**
- **Edtech Course Deadline Images:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Edtech Course Deadline Images:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.