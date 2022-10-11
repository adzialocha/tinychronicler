type NoteEvent = {
  channel: number;
  note: number;
  noteOn: boolean;
  velocity: number;
};

const context = new AudioContext();
const sources: { [name: string]: AudioBuffer } = {};

const gainNode = context.createGain();
gainNode.gain.value = 0.2;
gainNode.connect(context.destination);

async function fetchAudioSample(url: string): Promise<ArrayBuffer> {
  const response = await window.fetch(url);
  const buffer = await response.arrayBuffer();
  return buffer;
}

async function createAudioBuffer(url: string): Promise<AudioBuffer> {
  const arrayBuffer = await fetchAudioSample(url);
  const result = await context.decodeAudioData(arrayBuffer);
  return result;
}

export async function startInstruments() {
  const promises: Promise<AudioBuffer>[] = [
    createAudioBuffer('/samples/test-1.wav'),
    createAudioBuffer('/samples/test-2.wav'),
    createAudioBuffer('/samples/test-3.wav'),
    createAudioBuffer('/samples/test-4.wav'),
  ];

  const results = await Promise.all(promises);
  results.forEach((source, index) => {
    sources[`test-${index + 1}`] = source;
  });
}

export function stopInstruments() {
  // @TODO
}

export function triggerNote(event: NoteEvent) {
  if (event.noteOn) {
    const note = event.note % Object.keys(sources).length;
    const audioSource = context.createBufferSource();
    audioSource.buffer = sources[`test-${note + 1}`];
    audioSource.connect(gainNode);
    audioSource.start();
  }
}
