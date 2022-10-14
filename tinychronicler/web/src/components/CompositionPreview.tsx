import styled from 'styled-components';
import { Cutout } from 'react95';
import { useMemo } from 'react';

import type { Composition } from '~/types';

const Line = styled.p`
  display: flex;
  justify-content: space-between;
`;

const Character = styled.span`
  width: 50px;
  text-align: center;
`;

const Break = styled.span`
  height: 1em;
`;

const PreviewBox = ({ composition }: { composition: Composition }) => {
  const lines = useMemo(() => {
    if (!composition.score) {
      return [];
    }

    return composition.score.split('\n');
  }, [composition.score]);

  return (
    <div>
      {lines.map((line: string, index) => {
        return (
          <Line key={index}>
            {line === '' ? (
              <Break />
            ) : (
              line.split('').map((char, charIndex) => {
                return (
                  <Character key={`${index}-${charIndex}`}>{char}</Character>
                );
              })
            )}
          </Line>
        );
      })}
    </div>
  );
};

const CompositionPreview = ({ composition }: { composition: Composition }) => {
  return (
    <Cutout
      style={{
        backgroundColor: '#fff',
        height: '200px',
        width: '700px',
      }}
    >
      <PreviewBox composition={composition} />
    </Cutout>
  );
};

export default CompositionPreview;
