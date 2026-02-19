#!/usr/bin/env python3
"""
Hindi Voice Agent V6
- ONLY large Hindi STT model (no English confusion!)
- Mic mute during speech
- Fast AI responses
"""

import ollama, subprocess, os, time, json, audioop
from datetime import datetime
import pyaudio, vosk

SINK     = "bluez_output.F9_74_83_51_11_F5.1"
PIPER    = "./piper/piper"
VOICE    = "./models/hi_IN-priyamvada-medium.onnx"
MIC_CARD = "2"

is_speaking = False

# ── MIC MUTE ─────────────────────────────────────────────────────────
def mic_mute():
    for ctrl in ['Mic','Capture','Master','ADC']:
        r = subprocess.run(
            ['amixer','-c',MIC_CARD,'sset',ctrl,'0%'],
            capture_output=True
        )
        if r.returncode == 0:
            return

def mic_unmute():
    for ctrl in ['Mic','Capture','Master','ADC']:
        r = subprocess.run(
            ['amixer','-c',MIC_CARD,'sset',ctrl,'100%'],
            capture_output=True
        )
        if r.returncode == 0:
            return

# ── SPEAKER ──────────────────────────────────────────────────────────
def setup_speaker():
    for cmd in [
        ['pactl','set-default-sink',SINK],
        ['pactl','set-sink-volume', SINK,'70%'],
        ['wpctl','set-volume','@DEFAULT_AUDIO_SINK@','1.0'],
    ]:
        subprocess.run(cmd, capture_output=True, timeout=3)
    print("✓ Speaker: TG113")

# ── TTS ──────────────────────────────────────────────────────────────
def speak(text):
    global is_speaking
    text = text.replace('"','').replace("'",'').strip()
    if not text: return

    is_speaking = True
    mic_mute()

    try:
        tmp = '/tmp/out.wav'
        if os.path.exists(tmp): os.remove(tmp)
        cmd = (f'echo "{text}" | {PIPER} '
               f'--model {VOICE} '
               f'--length_scale 0.85 '
               f'-f {tmp} 2>/dev/null')
        subprocess.run(cmd, shell=True, timeout=12)
        if os.path.exists(tmp) and os.path.getsize(tmp)>100:
            subprocess.run(['paplay','--volume=65536',tmp],
                          capture_output=True, timeout=15)
            try: os.remove(tmp)
            except: pass
    except:
        subprocess.run(
            ['espeak-ng','-v','hi','-s','145',text],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    time.sleep(1.0)
    mic_unmute()
    is_speaking = False

# ── AI ───────────────────────────────────────────────────────────────
def get_model():
    r = subprocess.run(['ollama','list'],
                      capture_output=True, text=True)
    for m in ['llama3.2','gemma2','tinyllama']:
        for line in r.stdout.split('\n'):
            if m in line.lower() and line.strip():
                model = line.split()[0]
                print(f"✓ AI: {model}")
                return model
    print("❌ Run: ollama serve && ollama pull gemma2:2b")
    exit(1)

def ask_ai(q, model):
    now    = datetime.now()
    months = ['जनवरी','फरवरी','मार्च','अप्रैल','मई','जून',
             'जुलाई','अगस्त','सितंबर','अक्टूबर','नवंबर','दिसंबर']

    system = """तुम एक हिंदी आवाज़ सहायक हो।
सख्त नियम:
1. सिर्फ हिंदी में जवाब दो
2. एक वाक्य, 10 शब्द से कम
3. सही जानकारी दो
4. कोई अंग्रेजी नहीं
5. कोई * # emoji नहीं

सही जवाब के उदाहरण:
सवाल: तमिलनाडु के CM कौन हैं?
जवाब: तमिलनाडु के मुख्यमंत्री एम.के. स्टालिन हैं।

सवाल: AI क्या है?
जवाब: AI यानी कृत्रिम बुद्धिमत्ता एक कंप्यूटर तकनीक है।

सवाल: तुम्हें किसने बनाया?
जवाब: मुझे एक छात्र ने कॉलेज प्रोजेक्ट के लिए बनाया।"""

    prompt = (
        f"समय:{now.hour}:{now.minute:02d} "
        f"तारीख:{now.day} {months[now.month-1]}\n"
        f"सवाल: {q}"
    )

    try:
        r = ollama.chat(
            model=model,
            messages=[
                {'role':'system','content':system},
                {'role':'user',  'content':prompt}
            ],
            options={
                'num_predict'   : 30,
                'temperature'   : 0.1,
                'num_ctx'       : 512,
                'num_thread'    : 4,
                'top_k'         : 5,
                'repeat_penalty': 2.0,
            }
        )
        ans = r['message']['content'].strip()

        # Clean
        for ch in ['*','#','`','_','।।','"',"'"]:
            ans = ans.replace(ch,'')

        # First sentence only
        for sep in ['।','\n','. ']:
            if sep in ans:
                ans = ans.split(sep)[0].strip()
                if sep=='।': ans+='।'
                break

        # Remove prefixes
        for pre in ['जवाब:','उत्तर:','Answer:','A:']:
            if ans.startswith(pre):
                ans = ans[len(pre):].strip()

        # Must have Hindi chars
        hindi = sum(1 for c in ans
                   if '\u0900'<=c<='\u097F')
        if hindi < 2:
            return 'माफ़ करें, जानकारी नहीं है।'

        return ans if len(ans)>3 else 'माफ़ करें।'
    except Exception as e:
        print(f" [AI Error: {e}]", end="")
        return 'माफ़ करें, कोई समस्या हुई।'

# ── QUICK ANSWERS ─────────────────────────────────────────────────────
def quick_answer(text):
    tl     = text.lower().strip()
    now    = datetime.now()
    months = ['जनवरी','फरवरी','मार्च','अप्रैल','मई','जून',
             'जुलाई','अगस्त','सितंबर','अक्टूबर','नवंबर','दिसंबर']

    checks = [
        (['समय','बजे','time','what time','कितने'],
         f"अभी {now.hour} बजकर {now.minute} मिनट है।"),
        (['तारीख','आज','date','today'],
         f"आज {now.day} {months[now.month-1]} {now.year} है।"),
        (['तापमान','temperature','temp'],
         None),  # Dynamic below
        (['internet','इंटरनेट','online','wifi'],
         "नहीं, मैं पूरी तरह ऑफलाइन हूँ।"),
        (['नमस्ते','hello','hi','hey','हेलो'],
         "नमस्ते! बोलिए।"),
        (['धन्यवाद','thanks','शुक्रिया'],
         "आपका स्वागत है!"),
        (['अलविदा','bye','goodbye'],
         "अलविदा! फिर मिलेंगे!"),
        (['नाम','your name','तुम कौन','who are you'],
         "मेरा नाम सहायक है।"),
        (['मदद','help','क्या कर सकते'],
         "मैं हिंदी में सवालों के जवाब दे सकता हूँ।"),
    ]

    for keywords, response in checks:
        if any(w in tl for w in keywords):
            if response is None:
                # Temperature
                try:
                    with open('/sys/class/thermal/'
                             'thermal_zone0/temp') as f:
                        t = int(f.read())/1000
                    return f"तापमान {t:.0f} डिग्री है।"
                except:
                    return "तापमान जानकारी नहीं।"
            return response
    return None

# ── PROCESS ──────────────────────────────────────────────────────────
def process(text, model, metrics):
    t0  = time.time()
    ans = quick_answer(text)

    if ans:
        print(f"⚡ : {ans}")
        print("🔊 ", end="", flush=True)
        speak(ans)
        total = time.time()-t0
        print(f"✅ {total:.1f}s")
    else:
        print("🧠 ", end="", flush=True)
        t1  = time.time()
        ans = ask_ai(text, model)
        ai  = time.time()-t1
        print(f"{ai:.1f}s → {ans}")
        print("🔊 ", end="", flush=True)
        t2  = time.time()
        speak(ans)
        tts = time.time()-t2
        total = time.time()-t0
        st = "✅" if total<3 else("🔶" if total<5 else"❌")
        print(f"AI:{ai:.1f}s TTS:{tts:.1f}s "
              f"Tot:{total:.1f}s {st}")

    metrics.append(time.time()-t0)
    return ans

# ── VOICE MODE ───────────────────────────────────────────────────────
def voice_mode(model):
    global is_speaking

    # Find mic
    p = pyaudio.PyAudio()
    mic_idx, mic_rate = None, None
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            for rate in [16000, 48000, 44100]:
                try:
                    s = p.open(
                        format=pyaudio.paInt16,
                        channels=1, rate=rate,
                        input=True, input_device_index=i,
                        frames_per_buffer=2048
                    )
                    s.read(2048, exception_on_overflow=False)
                    s.close()
                    mic_idx  = i
                    mic_rate = rate
                    print(f"✓ Mic [{i}] @ {rate}Hz")
                    break
                except: continue
        if mic_idx is not None: break
    p.terminate()

    if mic_idx is None:
        print("❌ No mic found!")
        return

    # Load ONLY large Hindi model
    print("📚 Loading LARGE Hindi model (better accuracy)...")
    print("   (takes ~30 seconds to load)")

    # Use large model if available
    if os.path.exists("vosk-model-hi-0.22"):
        hi_model = vosk.Model("vosk-model-hi-0.22")
        print("✓ Large Hindi model loaded!")
    else:
        hi_model = vosk.Model("vosk-model-small-hi-0.22")
        print("✓ Small Hindi model loaded")

    p      = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1, rate=mic_rate,
        input=True, input_device_index=mic_idx,
        frames_per_buffer=8000
    )

    # HINDI ONLY recognizer
    rec = vosk.KaldiRecognizer(hi_model, 16000)
    rec.SetWords(True)

    metrics   = []
    last_part = ""

    def reset_rec():
        r = vosk.KaldiRecognizer(hi_model, 16000)
        r.SetWords(True)
        return r

    print("\n✅ READY!")
    print("─"*55)
    print("🎤 हिंदी में बोलिए! (Speak in Hindi)")
    print("💡 Hold mic close, speak clearly")
    print("💡 Wait for reply before speaking")
    print("बंद करो - stop the agent")
    print("─"*55+"\n")

    speak("नमस्ते! हिंदी में बोलिए।")

    try:
        while True:
            raw = stream.read(
                8000, exception_on_overflow=False
            )

            # Skip while speaking
            if is_speaking:
                rec = reset_rec()
                last_part = ""
                continue

            # Resample to 16kHz
            if mic_rate != 16000:
                raw, _ = audioop.ratecv(
                    raw, 2, 1, mic_rate, 16000, None
                )

            done = rec.AcceptWaveform(raw)

            if done:
                result = json.loads(rec.Result())
                text   = result.get('text','').strip()

                if len(text) < 2:
                    continue

                last_part = ""
                print(f"\r🎤 : {text:<55}")

                # Exit
                if any(w in text for w in
                       ['बंद करो','रोको','बंद']):
                    speak("अलविदा!")
                    break

                print(f"\n{'─'*50}")
                print(f"👤 : {text}")
                process(text, model, metrics)
                print("─"*50)
                print("\n🎤 बोलिए...")

                # Reset after each command
                rec = reset_rec()

            else:
                # Show partial
                partial = json.loads(
                    rec.PartialResult()
                ).get('partial','')
                if partial and partial != last_part:
                    print(f"\r🎙️  {partial:<55}",
                          end="", flush=True)
                    last_part = partial

    except KeyboardInterrupt:
        print("\n\n👋 Stopped")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    if metrics:
        avg = sum(metrics)/len(metrics)
        u3  = sum(1 for t in metrics if t<3)
        print(f"\n📊 Avg:{avg:.1f}s | <3s:{u3}/{len(metrics)}")

# ── TEXT MODE ────────────────────────────────────────────────────────
def text_mode(model):
    print("\n💬 TEXT MODE - Type Hindi or English")
    print("'exit' to quit\n")
    metrics = []
    while True:
        try:
            q = input("👤 You: ").strip()
            if not q: continue
            if q.lower()=='exit':
                speak("अलविदा!")
                break
            print("─"*50)
            process(q, model, metrics)
            print("─"*50+"\n")
        except KeyboardInterrupt:
            break
    if metrics:
        print(f"\n📊 Avg:{sum(metrics)/len(metrics):.1f}s")

# ── MAIN ─────────────────────────────────────────────────────────────
def main():
    print("\n"+"="*55)
    print("   🎯 HINDI VOICE AGENT V6")
    print("   Large Hindi STT + Mic Mute Fix")
    print("="*55+"\n")

    setup_speaker()

    # Make sure Ollama is running
    print("🔍 Checking Ollama...", end=" ")
    r = subprocess.run(['ollama','list'],
                      capture_output=True, text=True,
                      timeout=5)
    if r.returncode != 0:
        print("starting...")
        subprocess.Popen(['ollama','serve'],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        time.sleep(3)
    else:
        print("✓")

    model = get_model()

    print("🔥 Warming AI...", end=" ", flush=True)
    t = time.time()
    ollama.chat(model=model,
               messages=[{'role':'user','content':'hi'}],
               options={'num_predict':3,'num_thread':4})
    print(f"({time.time()-t:.1f}s)\n")

    print("1 = Text mode (keyboard)")
    print("2 = Voice mode (mic)")
    c = input("Choice: ").strip()

    if c == '2':
        voice_mode(model)
    else:
        text_mode(model)

main()
