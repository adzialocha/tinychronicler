import { createRef, useEffect } from 'react';
import { Cutout } from 'react95';

import type { Composition } from '~/types';

const CELL_SIZE = 10;
const MARKER_SEC = 30;

const CompositionPreview = ({ composition }: { composition: Composition }) => {
  const canvasRef = createRef<HTMLCanvasElement>();

  useEffect(() => {
    if (!composition.data) {
      return;
    }

    const { notes, parameters } = composition.data;
    const end = Math.ceil(notes[notes.length - 1][1]);

    const canvas = canvasRef.current;

    if (!canvas) {
      return;
    }

    canvas.setAttribute('width', `${end * CELL_SIZE + 10}px`);

    const context = canvas.getContext('2d');

    if (!context) {
      return;
    }

    const { width, height } = context.canvas;

    // Draw background
    context.fillStyle = '#fff';
    context.fillRect(0, 0, width, height);

    // Draw markers
    context.fillStyle = '#999';
    context.strokeStyle = '#999';
    context.lineWidth = 2;
    const steps = Math.ceil(end / MARKER_SEC);
    for (let i = 0; i < steps; i += 1) {
      const pos = i * MARKER_SEC * CELL_SIZE;
      context.beginPath();
      context.moveTo(pos, 0);
      context.lineTo(pos, 178);
      context.stroke();
      context.fillText(`${i * MARKER_SEC}`, pos + 5, 10);
    }

    // Draw note events
    context.fillStyle = '#000';
    notes.forEach((note) => {
      const from = Math.round(note[0] * CELL_SIZE);
      const to = Math.round(note[1] * CELL_SIZE) - from;
      context.fillRect(from, 20, to, CELL_SIZE * 3);
    });

    // Draw parameter events
    parameters.forEach((parameter) => {
      context.fillStyle = `rgba(${Math.floor(
        Math.random() * 255,
      )}, ${Math.floor(Math.random() * 255)}, ${Math.floor(
        Math.random() * 255,
      )}, 0.5)`;
      const from = Math.round(parameter.module[0] * CELL_SIZE);
      const to = Math.round(parameter.module[1] * CELL_SIZE) - from;
      context.fillRect(from, 70, to, CELL_SIZE * 10);
      context.fillText(parameter.parameters.join(', '), from + 5, 70);
    });
  }, [canvasRef, composition.data]);

  return (
    <Cutout
      style={{ width: '700px', height: '200px', backgroundColor: '#fff' }}
    >
      <canvas height={178} ref={canvasRef} />
    </Cutout>
  );
};

export default CompositionPreview;
