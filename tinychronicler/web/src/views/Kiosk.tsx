import { createElement, useEffect, useState, useMemo, useRef } from 'react';
import styled from 'styled-components';
import OSC from 'osc-js';

const OSC_ENDPOINT = '127.0.0.1';
const OSC_PORT = '8000/ws';
const RECONNECTION_ATTEMPT_INTERVAL = 5000;

type VisualState =
  | {
      mode: 'black';
    }
  | ({
      mode: 'image';
    } & ImageArgs)
  | ({
      mode: 'video';
    } & VideoArgs);

type AudioState = {
  url?: string;
};

type VideoArgs = {
  url: string;
  seek: number;
  duration: number;
  muted: boolean;
};

type ImageArgs = {
  url: string;
  duration: number;
};

type AudioArgs = {
  url: string;
};

const StyledKiosk = styled.div`
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background-color: #000;
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
`;

const Image = styled.img`
  object-fit: contain;
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
`;

const Video = styled.video`
  object-fit: contain;
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
`;

const Audio = styled.audio`
  display: none;
`;

const ImageView = (props: ImageArgs) => {
  return <Image src={props.url} />;
};

const VideoPlayer = (props: VideoArgs) => {
  return <Video autoPlay muted={props.muted} loop src={props.url} />;
};

const AudioPlayer = (props: AudioArgs) => {
  return <Audio autoPlay src={props.url} />;
};

const Kiosk = () => {
  const [visualState, setVisualState] = useState<VisualState>({
    mode: 'black',
  });
  const [audioState, setAudioState] = useState<AudioState>({
    url: undefined,
  });

  const osc = useMemo(() => {
    return new OSC();
  }, []);

  const onVideo = (args: VideoArgs) => {
    setVisualState({
      mode: 'video',
      ...args,
    });
  };

  const onImage = (args: ImageArgs) => {
    setVisualState({
      mode: 'image',
      ...args,
    });
  };

  const onAudio = (args: AudioArgs) => {
    setAudioState({
      ...args,
    });
  };

  const onResetVideo = () => {
    setVisualState({
      mode: 'black',
    });
  };

  const onResetAudio = () => {
    setAudioState({
      url: undefined,
    });
  };

  useEffect(() => {
    let timeout: number | undefined;

    const reattempt = () => {
      if (timeout !== undefined) {
        return;
      }

      timeout = window.setTimeout(() => {
        timeout = undefined;
        connect();
      }, RECONNECTION_ATTEMPT_INTERVAL);
    };

    const clearTimeout = () => {
      if (timeout === undefined) {
        return;
      }

      window.clearTimeout(timeout);
      timeout = undefined;
    };

    const connect = () => {
      console.info('OSC client trying to connect ..');

      osc.open({
        host: OSC_ENDPOINT,
        port: OSC_PORT,
      });
    };

    osc.on('open', () => {
      console.info('OSC client ready');
      clearTimeout();
    });

    osc.on('close', () => {
      console.info('OSC client close');
      // Attempt to re-connect
      reattempt();
    });

    osc.on('/video', (message: OSC.Message) => {
      const [url, seek, duration, muted] = message.args;

      onVideo({
        url: url as string,
        seek: seek as number,
        duration: duration as number,
        muted: muted as boolean,
      });
    });

    osc.on('/video/reset', () => {
      onResetVideo();
    });

    osc.on('/image', (message: OSC.Message) => {
      const [url, duration] = message.args;

      onImage({
        url: url as string,
        duration: duration as number,
      });
    });

    osc.on('/audio', (message: OSC.Message) => {
      onAudio({
        url: message.args[0] as string,
      });
    });

    osc.on('/audio/reset', () => {
      onResetAudio();
    });

    connect();

    return () => {
      osc.close();
      clearTimeout();
    };
  }, [osc]);

  return (
    <StyledKiosk>
      {audioState.url && <AudioPlayer url={audioState.url} />}
      {visualState.mode === 'video' && <VideoPlayer {...visualState} />}
      {visualState.mode === 'image' && <ImageView {...visualState} />}
    </StyledKiosk>
  );
};

export default Kiosk;
