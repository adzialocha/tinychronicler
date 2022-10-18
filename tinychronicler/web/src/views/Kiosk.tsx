import React, { useEffect, useState, useMemo, useRef } from 'react';
import styled from 'styled-components';
import OSC from 'osc-js';

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

type VideoArgs = {
  url: string;
  seek: number;
};

type ImageArgs = {
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

const ImageView = React.forwardRef<HTMLImageElement, Visible>((props, ref) => {
  return <Image visible={props.visible} ref={ref} />;
});

const VideoPlayer = React.forwardRef<HTMLVideoElement, Visible>(
  (props, ref) => {
    return <Video visible={props.visible} ref={ref} loop muted />;
  },
);

const Kiosk = () => {
  const imageRef = useRef<HTMLImageElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);

  const [visualState, setVisualState] = useState<VisualState>({
    mode: 'black',
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

  const onResetVideo = () => {
    setVisualState({
      mode: 'black',
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

      if (window.location.host === 'tinychronicler.local') {
        osc.open({
          host: 'tinychronicler.local',
          port: '8000/ws',
        });
      } else {
        osc.open({
          host: '127.0.0.1',
          port: '8000/ws',
        });
      }
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
      const [url, seek] = message.args;

      onVideo({
        url: url as string,
        seek: seek as number,
      });
    });

    osc.on('/video/reset', () => {
      onResetVideo();
    });

    osc.on('/image', (message: OSC.Message) => {
      const [url] = message.args;

      onImage({
        url: url as string,
      });
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

  return (
    <StyledKiosk>
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
