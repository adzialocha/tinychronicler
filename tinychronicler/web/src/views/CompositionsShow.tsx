import { useParams } from 'react-router-dom';
import {
  Fieldset,
  Hourglass,
  Window,
  WindowContent,
  WindowHeader,
} from 'react95';

import CompositionPreview from '~/components/CompositionPreview';
import useComposition from '~/hooks/useComposition';
import { formatDate } from '~/utils/format';

const CompositionsShow = () => {
  const { id, chronicleId } = useParams();
  const { composition, loading } = useComposition(chronicleId, id);

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
      </WindowContent>
    </Window>
  );
};

export default CompositionsShow;
