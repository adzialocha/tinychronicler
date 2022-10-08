import { useEffect, useState, useCallback, useMemo } from 'react';
import styled from 'styled-components';
import OSC from 'osc-js';

const OSC_ENDPOINT = '127.0.0.1';
const OSC_PORT = '8000/ws';
const RECONNECTION_ATTEMPT_INTERVAL = 5000;

const MODE_STANDBY = 0;
const MODE_VIDEO = 1;
const MODE_IMAGE = 2;

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
`;

const ImageView = () => {
  return null;
};

const VideoPlayer = () => {
  return null;
};

const AudioPlayer = () => {
  return null;
};

const Kiosk = () => {
  const [mode, setMode] = useState(MODE_STANDBY);

  const osc = useMemo(() => {
    return new OSC();
  }, []);

  const onVideo = (args: VideoArgs) => {
    setMode(MODE_VIDEO);
    console.log(args);
  };

  const onImage = (args: ImageArgs) => {
    setMode(MODE_IMAGE);
    console.log(args);
  };

  const onAudio = (args: AudioArgs) => {
    console.log(args);
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
      setMode(MODE_STANDBY);
    });

    osc.on('/image', (message: OSC.Message) => {
      const [url, duration] = message.args;

      onImage({
        url: url as string,
        duration: duration as number,
      });
    });

    osc.on('/image/reset', () => {
      setMode(MODE_STANDBY);
    });

    osc.on('/audio', (message: OSC.Message) => {
      onAudio({
        url: message.args[0] as string,
      });
    });

    connect();

    return () => {
      osc.close();
      clearTimeout();
    };
  }, [osc]);

  return (
    <StyledKiosk>
      <AudioPlayer />
      {mode === MODE_VIDEO && <VideoPlayer />}
      {mode === MODE_IMAGE && <ImageView />}
    </StyledKiosk>
  );
};

export default Kiosk;
