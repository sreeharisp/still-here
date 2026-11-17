# Still Here

**Forgotten Cosmos · An interactive museum of what remains**

A storytelling project created for the NASA Space Apps challenge “Abandoned but not Forgotten: Storytelling about NASA's Discarded Equipment on the Moon and Mars.”

Explore the stories of equipment left on other worlds, with clearly labeled imagined narration and NASA-sourced facts. This is an independent educational project, not an official NASA product or an endorsement by NASA.

## Explore

- [Live website](https://vocal-starship-0390bb.netlify.app/)
- [Seven-slide presentation](https://vocal-starship-0390bb.netlify.app/demo.html)
- [GitHub repository](https://github.com/sreeharisp/still-here)

## The collection

- Opportunity and Spirit: rover journeys and scientific discoveries on Mars.
- Apollo 15 lunar rover: expanding the reach of lunar exploration.
- Apollo 15 hammer and feather: a memorable demonstration of gravitational acceleration.
- Apollo retroreflectors: a contrast case showing that equipment left behind is not necessarily discarded or inactive.

The museum includes Moon/Mars filters, fact panels, source links, a quiz, and optional browser text-to-speech.

## Run locally

Download or clone [this repository](https://github.com/sreeharisp/still-here), then open [`index.html`](index.html) in a browser. Open [`demo.html`](demo.html) for the presentation. No package installation or server is required.

Presentation controls: Previous/Next, Left/Right arrows, Page Up/Page Down, and Home/End. To export a PDF, select A4 landscape and disable browser headers and footers; check the print preview for seven pages.

The pages are self-contained. External NASA references require internet access. Optional speech depends on browser/device support and may use an online speech service.

## Technology

HTML, CSS, JavaScript, and inline SVG; no external JavaScript libraries or build process.

## Sources and responsible storytelling

The website links to NASA Science, NASA NSSDCA, NASA/JPL, and NASA's lunar laser-ranging explanation. Its sources section explains which measurements and findings each reference supports.

First-person stories are fictional interpretations, not historical quotations. Schematic illustrations are not photographs, precise maps, or engineering models. Evidence of ancient water or potentially habitable environments is not presented as proof of life.

## AI disclosure

An OpenAI assistant in Zed assisted with code, writing, visual design, and schematic illustrations. AI-generated illustrations are labeled in the museum. Optional narration uses browser/device synthetic speech, not astronaut recordings. AI-generated text is not an independent factual source.

## Submission status and limitations

Publishing this repository or the website does not submit an entry to NASA Space Apps. Team members must review the work, complete the official submission, and verify current event requirements and deadlines.

**NASA resource qualification is pending.** The official challenge Resources list could not be retrieved during preparation. At least one source must be verified against that list and meaningfully used; NASA citations alone do not establish eligibility. See [SUBMISSION.md](SUBMISSION.md) for guidance and remaining checks.

No completed user study or measured educational impact is claimed. Check browser interactions, read-aloud, and presentation print layout manually before submitting.

## Optional technical checks

With Python installed:

```text
python validate.py --static-only
```

This checks local links, unique IDs, slide count, and external code dependencies. `python validate.py` also attempts interaction tests using Chrome or Edge in standard Windows installation locations. Static checks do not verify browser behavior, external URL availability, accessibility, or print layout. An earlier headless browser attempt is documented as timed out; no successful browser-interaction test is claimed.
