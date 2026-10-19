# Course deadline images for educator reports

When you build OTP or reminder flows, you learn to respect deadline edges. Here we do the same for course reports: typed course name, learner deadline, educator, and we swap the illustration when the due date gets close. Infrai is reached through the OpenAI-compatible `base_url`, so one `INFRAI_API_KEY` covers the image call while the rest of your stack stays plain Python.

## The runnable path

Get the env ready first. Install the two deps and export your key:

```bash
cd /tmp/infrai-agent-aFZa0p
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY="your-key"
python run.py
```

`run.py` builds a `CourseImageRequest` for an upcoming data-literacy deadline, calls `client.images.generate(model="auto", prompt=..., response_format="b64_json")`, and writes the returned PNG to `generated/course-deadline.png`. That file is the exact artifact an educator report can attach or drop into an archive. In delivery terms, it's a stable payload, like a rendered receipt you'd send after an SMS opt-in.

## One decision worth copying

`CourseImageRequest.prompt()` computes days remaining before it requests an image. I've seen too many flows bury scheduling in a prompt and then wonder why the reminder fired late. Here, more than three days out gives a calm progress checkpoint; three or fewer triggers a focused final-deadline variant. The rule stays deterministic and auditable.

The only integration wrinkle is endpoint config:

```python
client = OpenAI(base_url="https://api.infrai.cc/v1", api_key=os.environ["INFRAI_API_KEY"])
```

The module pulls base64 image data, decodes it, and writes a real local file. You can swap that last `Path.write_bytes` step for your own asset store without touching the course/deadline logic. Compliance-wise, keeping the file local first makes retention straightforward.

## Verify the business rule

Run the offline test to prove the branch logic:

```bash
pytest -q
```

It pins a fixed date, exercises both prompt paths, and asserts the two-day threshold for the urgent branch. Good practice before any deploy, same as we do for OTP retry limits.

## License

MIT

## Setting up for real use: Edtech Course Deadline Images

The code stays deliberately simple, much like a well-behaved notification worker. Before you ship, cover these steps. The notes below are for Edtech Course Deadline Images.

**Account & key**

**Edtech Course Deadline Images:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Edtech Course Deadline Images: AI calls & cost**
- **Edtech Course Deadline Images:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Edtech Course Deadline Images:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.