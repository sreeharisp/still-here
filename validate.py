"""Local checks using Python's standard library and installed Chrome/Edge.
Run: python validate.py
No network requests are needed by these tests. Speech and print layout need manual checks.
"""
from pathlib import Path
from html.parser import HTMLParser
import argparse
import html
import json
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
arguments = argparse.ArgumentParser(description=__doc__)
arguments.add_argument('--static-only', action='store_true', help='Skip browser launch')
options = arguments.parse_args()


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.slides = 0
        self.references = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for attribute in ('aria-labelledby', 'aria-describedby', 'aria-controls'):
            self.references.extend(attrs.get(attribute, '').split())
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
        if 'slide' in attrs.get('class', '').split():
            self.slides += 1
        assert not (tag == 'script' and 'src' in attrs), 'External JavaScript dependency'
        assert not (tag == 'link' and attrs.get('rel') == 'stylesheet'), 'External stylesheet'


for filename in ('index.html', 'demo.html'):
    parser = Page()
    parser.feed((ROOT / filename).read_text(encoding='utf-8'))
    assert len(parser.ids) == len(set(parser.ids)), f'Duplicate IDs: {filename}'
    for reference in parser.references:
        assert reference in parser.ids, f'Missing accessibility target: {reference}'
    for link in parser.links:
        if link.startswith('#'):
            assert not link[1:] or link[1:] in parser.ids, f'Missing anchor: {link}'
        elif '://' not in link:
            assert (ROOT / link).is_file(), f'Missing local file: {link}'
    if filename == 'demo.html':
        assert parser.slides == 7, f'Expected seven slides, found {parser.slides}'
    print(f'PASS {filename}: unique IDs, local links, no external code dependencies')

if options.static_only:
    raise SystemExit(0)

browser = next((p for p in (
    Path('C:/Program Files/Google/Chrome/Application/chrome.exe'),
    Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'),
    Path('C:/Program Files/Microsoft/Edge/Application/msedge.exe'),
) if p.is_file()), None)
if browser is None:
    raise SystemExit('Static checks passed; browser tests skipped: Chrome/Edge not found.')

MUSEUM_TEST = r"""
const check=(condition,message)=>{if(!condition)throw Error(message);};
const click=selector=>{const element=document.querySelector(selector);check(element,'Missing '+selector);element.click();};
check(document.querySelector('#story-title').textContent==='Opportunity','Initial story');
check(document.querySelector('#object-art').innerHTML.includes('ellipse'),'Initial illustration');
click('[data-filter="moon"]');
check([...document.querySelectorAll('.artifact-button:not([hidden])')].length===3,'Moon filter');
check(document.querySelector('#story-title').textContent==='The lunar rover','Filter selects valid story');
check(document.querySelector('#story-announcement').textContent.includes('The lunar rover'),'Story change announced');
click('[data-id="hammer"]');
check(document.querySelector('#narration').textContent.includes('David Scott'),'Hammer narrative');
click('#next');
check(document.querySelector('#story-title').textContent==='The quiet reflector','Filtered next');
click('#next');
check(document.querySelector('#story-title').textContent==='The lunar rover','Filtered wrap');
click('[data-filter="mars"]');
check([...document.querySelectorAll('.artifact-button:not([hidden])')].length===2,'Mars filter');
click('[data-id="spirit"]');
check(document.querySelector('#facts').textContent.includes('7.73'),'Spirit facts');
check(document.querySelector('#story-source').href.includes('spirit-rover'),'Story source');
click('[data-filter="all"]');
check([...document.querySelectorAll('.artifact-button:not([hidden])')].length===5,'All filter');
check(document.querySelector('#progress').textContent.startsWith('5 of 5'),'Visited counter');
click('[data-answer="hammer"]');
check(document.querySelector('#quiz-feedback').textContent.startsWith('Not quite'),'Wrong answer feedback');
click('[data-answer="reflector"]');
check(document.querySelector('#quiz-feedback').textContent.startsWith('Exactly'),'Correct answer feedback');
for(const button of document.querySelectorAll('.artifact-button')){
 button.click();
 check(document.querySelectorAll('.artifact-button[aria-pressed="true"]').length===1,'Selection state');
 check(document.querySelectorAll('#facts>div').length===3,'Three fact panels');
 check(document.querySelector('#object-art').innerHTML.length>100,'Object drawing');
 check(!document.querySelector('.scene').scrollWidth || document.documentElement.scrollWidth<=window.innerWidth,'No horizontal page overflow');
}
const spoken=[];
Object.defineProperty(window,'speechSynthesis',{configurable:true,value:{cancel(){},speak(utterance){spoken.push(utterance);}}});
Object.defineProperty(window,'SpeechSynthesisUtterance',{configurable:true,value:class {constructor(text){this.text=text;}}});
click('#listen');
check(document.querySelector('#listen').getAttribute('aria-pressed')==='true','Speech start state');
const oldSpeech=spoken[0];
click('[data-id="spirit"]');
check(document.querySelector('#listen').getAttribute('aria-pressed')==='false','Story change cancels speech');
oldSpeech.onerror();
check(document.querySelector('#audio-status').textContent==='','Ignore canceled speech error');
click('#listen');
oldSpeech.onend();
check(document.querySelector('#listen').getAttribute('aria-pressed')==='true','Old completion cannot stop new speech');
spoken[1].onend();
check(document.querySelector('#audio-status').textContent==='Story finished.','Current speech completion');
click('#listen');
click('#listen');
spoken[2].onerror();
check(document.querySelector('#audio-status').textContent==='','Manual stop ignores late error');
"""
DEMO_TEST = r"""
const check=(condition,message)=>{if(!condition)throw Error(message);};
const visible=()=>[...document.querySelectorAll('.slide')].filter(s=>!s.hidden);
check(visible().length===1,'One visible slide');
check(document.querySelector('#prev').disabled,'Previous disabled on first');
document.querySelector('#next').click();
check(document.querySelector('#counter').textContent.startsWith('Slide 2 of 7'),'Next button');
document.dispatchEvent(new KeyboardEvent('keydown',{key:'End',bubbles:true}));
check(document.querySelector('#counter').textContent.startsWith('Slide 7 of 7'),'End key');
check(document.querySelector('#next').disabled,'Next disabled on last');
document.dispatchEvent(new KeyboardEvent('keydown',{key:'Home',bubbles:true}));
check(document.querySelector('#counter').textContent.startsWith('Slide 1 of 7'),'Home key');
document.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));
check(document.querySelector('#counter').textContent.startsWith('Slide 2 of 7'),'Arrow key');
check(visible().length===1,'Exactly one slide after navigation');
check(document.documentElement.scrollWidth<=window.innerWidth,'No horizontal page overflow');
"""

for filename, test in (('index.html', MUSEUM_TEST), ('demo.html', DEMO_TEST)):
    for width in (1280, 390, 320):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temporary:
            temp = Path(temporary)
            source = (ROOT / filename).read_text(encoding='utf-8')
            harness = """<script>
window.addEventListener('load',()=>{
const output=document.createElement('pre');output.id='validation-result';
try { TEST_BODY
output.textContent=JSON.stringify({pass:true});
} catch(error) {output.textContent=JSON.stringify({pass:false,error:String(error)});}
document.body.append(output);
});
</script>""".replace('TEST_BODY', test)
            page = temp / 'test.html'
            page.write_text(source.replace('</body>', harness + '</body>'), encoding='utf-8')
            try:
                result = subprocess.run([
                    str(browser), '--headless', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--disable-background-networking',
                    '--allow-file-access-from-files', '--dump-dom',
                    '--virtual-time-budget=1500', f'--window-size={width},900',
                    '--hide-scrollbars', f'--user-data-dir={temp / "profile"}',
                    page.as_uri(),
                ], capture_output=True, timeout=25)
            except subprocess.TimeoutExpired:
                raise SystemExit('Browser checks could not finish: headless browser timed out after 25 seconds. Static checks passed. Open the HTML files manually to check interaction and layout.')
            output = result.stdout.decode('utf-8', errors='replace')
            match = re.search(r'<pre id="validation-result">(.*?)</pre>', output, re.S)
            if not match:
                raise AssertionError('Browser did not return test results: ' +
                                     result.stderr.decode('utf-8', errors='replace')[-1500:])
            report = json.loads(html.unescape(match.group(1)))
            assert report['pass'], f'{filename} at {width}px: {report}'
            print(f'PASS {filename}: browser interaction checks at {width}px')
print('All automated checks passed. Audio, visual design, external URLs and print pagination require manual review.')
