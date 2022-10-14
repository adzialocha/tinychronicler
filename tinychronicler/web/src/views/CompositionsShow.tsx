import { useParams } from 'react-router-dom';
import {
  Button,
  Fieldset,
  Hourglass,
  Window,
  WindowContent,
  WindowHeader,
} from 'react95';

import CompositionPreview from '~/components/CompositionPreview';
import useComposition from '~/hooks/useComposition';
import { formatDate } from '~/utils/format';
import request from '~/utils/api';

const CompositionsShow = () => {
  const { id, chronicleId } = useParams();
  const { composition, loading } = useComposition(chronicleId, id);

  const onPlay = async (isDemo = false) => {
    if (!chronicleId || !id) {
      return;
    }

    try {
      await request(
        [
          'chronicles',
          chronicleId.toString(),
          'compositions',
          id.toString(),
          'play',
        ],
        {
          is_demo: isDemo,
        },
        'POST',
      );
    } catch (error) {
      window.alert(error);
    }
  };

  const onPrint = async () => {
    if (!chronicleId || !id) {
      return;
    }

    try {
      await request(
        [
          'chronicles',
          chronicleId.toString(),
          'compositions',
          id.toString(),
          'print',
        ],
        undefined,
        'POST',
      );
    } catch (error) {
      window.alert(error);
    }
  };

  const onStop = async () => {
    try {
      await request(['settings', 'stop'], undefined, 'POST');
    } catch (error) {
      window.alert(error);
    }
  };

  return loading ? (
    <Hourglass />
  ) : (
    <Window style={{ maxWidth: 800, minWidth: 800 }}>
      <WindowHeader>{composition.title}</WindowHeader>
      <WindowContent>
        <Fieldset label="Preview">
          <CompositionPreview composition={composition} />
        </Fieldset>
        <br />
        <Fieldset label="Meta">
          Version: {composition.version}
          <br />
          Generated: {formatDate(composition.created_at)}
          <br />
          Status: {composition.is_ready ? 'Ready' : 'Pending'}
        </Fieldset>
        <br />
        <Fieldset label="Tiny Chronicler 💌">
          <Button onClick={() => onPrint()}>🖨️ Print score</Button>
          <Button onClick={() => onPlay(true)}>🧪 Simulation</Button>
          <Button onClick={() => onPlay()}>🏓 Play composition</Button>
          <Button onClick={() => onStop()}>✋ Stop performance</Button>
        </Fieldset>
      </WindowContent>
    </Window>
  );
};

export default CompositionsShow;
