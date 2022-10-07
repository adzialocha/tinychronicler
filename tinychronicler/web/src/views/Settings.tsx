import { Fragment } from 'react';
import { Button, Fieldset, Window, WindowContent, WindowHeader } from 'react95';

import request from '~/utils/api';

const Settings = () => {
  const onTest = async (name: string) => {
    try {
      await request(
        ['settings', 'tests'],
        {
          name,
        },
        'POST',
      );
    } catch (error) {
      window.alert(error);
    }
  };

  return (
    <Fragment>
      <Window style={{ width: '100%', maxWidth: 600 }}>
        <WindowHeader>Settings</WindowHeader>
        <WindowContent>
          <Fieldset label="I/O Tests">
            <p>Thermal Printer</p>
            <Button onClick={() => onTest('print-test-page')}>
              Print test page
            </Button>
            <p>Video Output</p>
            <Button onClick={() => onTest('play-random-video')}>
              Play random video
            </Button>
            <Button onClick={() => onTest('show-random-image')}>
              Show random image
            </Button>
            <Button onClick={() => onTest('stop-video')}>
              Stop video / image output
            </Button>
            <p>Audio Output</p>
            <Button onClick={() => onTest('play-random-audio')}>
              Play random audio
            </Button>
            <Button onClick={() => onTest('stop-audio')}>
              Stop audio output
            </Button>
            <p>LED Matrix</p>
            <Button onClick={() => onTest('run-led-test')}>
              Run LED matrix test
            </Button>
          </Fieldset>
        </WindowContent>
      </Window>
    </Fragment>
  );
};

export default Settings;
