import React, { useEffect, useState, useMemo, useRef } from 'react';
import styled from 'styled-components';
import OSC from 'osc-js';

const OSC_ENDPOINT = '127.0.0.1';
const OSC_PORT = '8000/ws';

const RECONNECTION_ATTEMPT_INTERVAL = 5000;
const TRANSITION_DURATION = '100ms';

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

type Visible = {
  visible: boolean;
};

const Container = styled.div`
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  z-index: 1000;
  display: flex;
`;

const StyledKiosk = styled(Container)`
  background-color: #000;
`;

const Image = styled.img<Visible>`
  object-fit: contain;
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  opacity: ${(props) => (props.visible ? 1 : 0)};
  transition: opacity ${TRANSITION_DURATION} linear;
`;

const Video = styled.video<Visible>`
  object-fit: contain;
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  opacity: ${(props) => (props.visible ? 1 : 0)};
  transition: opacity ${TRANSITION_DURATION} linear;
`;

const Audio = styled.audio`
  display: none;
`;

const ImageView = React.forwardRef<HTMLImageElement, Visible>((props, ref) => {
  return <Image visible={props.visible} ref={ref} />;
});

const VideoPlayer = React.forwardRef<HTMLVideoElement, Visible>(
  (props, ref) => {
    return <Video visible={props.visible} ref={ref} loop />;
  },
);

const AudioPlayer = React.forwardRef<HTMLAudioElement>((_, ref) => {
  return <Audio ref={ref} autoPlay />;
});

const Kiosk = () => {
  const audioRef = useRef<HTMLAudioElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);

  const [visualState, setVisualState] = useState<VisualState>({
    mode: 'black',
  });
  const [audioState, setAudioState] = useState<AudioState>({
    url: undefined,
  });

  const startVideo = (args: VideoArgs) => {
    if (!videoRef.current) {
      return;
    }

    const video = videoRef.current;

    // Reset source first when changing video, otherwise the old video will be
    // visible during the fading css transition
    if (video.src !== args.url) {
      video.src = '';
    }

    video.src = args.url;
    video.currentTime = args.seek;
    video.muted = args.muted;
    video.play();
  };

  const stopVideo = () => {
    if (!videoRef.current) {
      return;
    }

    const video = videoRef.current;
    video.pause();
  };

  const showImage = (args: ImageArgs) => {
    if (!imageRef.current) {
      return;
    }

    const image = imageRef.current;

    // Reset source first when changing image, otherwise the old image will be
    // visible during the fading css transition
    if (image.src !== args.url) {
      image.src = '';
    }

    image.src = args.url;
  };

  const hideImage = () => {
    if (!imageRef.current) {
      return;
    }

    // Do nothing
  };

  const startAudio = (args: AudioArgs) => {
    if (!audioRef.current) {
      return;
    }

    const audio = audioRef.current;
    audio.src = args.url;
    audio.currentTime = 0;
    audio.play();
  };

  const stopAudio = () => {
    if (!audioRef.current) {
      return;
    }

    const audio = audioRef.current;
    audio.pause();
  };

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

    osc.on('*', (message: OSC.Message) => {
      console.log(message);
    });

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

  useEffect(() => {
    if (visualState.mode === 'video') {
      hideImage();
      startVideo(visualState);
    } else if (visualState.mode === 'image') {
      stopVideo();
      showImage(visualState);
    } else if (visualState.mode === 'black') {
      hideImage();
      stopVideo();
    }
  }, [visualState]);

  useEffect(() => {
    if (audioState.url) {
      startAudio({
        url: audioState.url,
      });
    } else {
      stopAudio();
    }
  }, [audioState]);

  return (
    <StyledKiosk>
      <AudioPlayer ref={audioRef} />
      <Container>
        <VideoPlayer ref={videoRef} visible={visualState.mode === 'video'} />
      </Container>
      <Container>
        <ImageView ref={imageRef} visible={visualState.mode === 'image'} />
      </Container>
    </StyledKiosk>
  );
};

export default Kiosk;
