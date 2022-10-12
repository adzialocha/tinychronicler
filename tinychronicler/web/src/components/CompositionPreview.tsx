import { useEffect } from 'react';
import { Cutout } from 'react95';

import type { Composition } from '~/types';

const CompositionCanvas = ({ composition }: { composition: Composition }) => {
  useEffect(() => {
    if (!composition.data) {
      return;
    }

    // @TODO
    // const { notes, parameters } = composition.data;
  }, [composition.data]);

  return <div />;
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
      <CompositionCanvas composition={composition} />
    </Cutout>
  );
};

export default CompositionPreview;
