import { createRef, useEffect } from 'react';
import { Cutout } from 'react95';

import type { Composition } from '~/types';

const CELL_SIZE = 10;
const MARKER_SEC = 30;

const CompositionCanvas = ({
  composition,
  from,
  to,
}: {
  composition: Composition;
  from: number;
  to: number;
}) => {
  const canvasRef = createRef<HTMLCanvasElement>();

  useEffect(() => {
    if (!composition.data) {
      return;
    }

    const { notes, parameters } = composition.data;

    if (notes.length <= from) {
      return;
    }

    const start = Math.ceil(notes[from][0]);
    const end =
      notes.length <= to
        ? Math.ceil(notes[notes.length - 1][1])
        : Math.ceil(notes[to][1]);
    const duration = end - start;

    const canvas = canvasRef.current;

    if (!canvas) {
      return;
    }

    canvas.setAttribute('width', `${duration * CELL_SIZE}px`);

    const context = canvas.getContext('2d');

    if (!context) {
      return;
    }

    const { width, height } = context.canvas;

    // Draw background
    context.fillStyle = '#fff';
    context.fillRect(0, 0, width, height);

    function xPos(x: number) {
      return Math.round((x - start) * CELL_SIZE);
    }

    // Draw markers
    context.fillStyle = '#999';
    context.strokeStyle = '#999';
    context.lineWidth = 2;
    const steps = Math.ceil(duration / MARKER_SEC);
    for (let i = 0; i < steps; i += 1) {
      const pos = xPos(i * MARKER_SEC);
      context.beginPath();
      context.moveTo(pos, 0);
      context.lineTo(pos, 178);
      context.stroke();
      context.fillText(`${i * MARKER_SEC}`, pos + 5, 10);
    }

    // Draw note events
    context.fillStyle = '#000';
    notes.forEach((note) => {
      const from = xPos(note[0]);
      const to = xPos(note[1]) - from;
      context.fillRect(from, 20, to, CELL_SIZE * 3);
    });

    // Draw parameter events
    parameters.forEach((parameter) => {
      context.fillStyle = `rgba(${Math.floor(
        Math.random() * 255,
      )}, ${Math.floor(Math.random() * 255)}, ${Math.floor(
        Math.random() * 255,
      )}, 0.5)`;
      const from = xPos(parameter.module[0]);
      const to = xPos(parameter.module[1]) - from;
      context.fillRect(from, 70, to, CELL_SIZE * 10);
      context.fillText(parameter.parameters.join(', '), from + 5, 70);
    });
  }, [canvasRef, composition.data, from, to]);

  return <canvas height={178} ref={canvasRef} />;
};

const CompositionPreview = ({ composition }: { composition: Composition }) => {
  return (
    <Cutout
      style={{
        backgroundColor: '#fff',
        height: '200px',
        width: '700px',
        whiteSpace: 'nowrap',
      }}
    >
      <CompositionCanvas composition={composition} from={0} to={500} />
      <CompositionCanvas composition={composition} from={500} to={1000} />
    </Cutout>
  );
};

export default CompositionPreview;
