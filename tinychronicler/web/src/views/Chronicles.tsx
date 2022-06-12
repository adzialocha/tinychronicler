import { Fragment, useEffect, useState } from 'react';
import { DateTime } from 'luxon';

import request from '~/utils/api';

type Chronicle = {
  id: number;
  title: string;
  description: string;
  created_at: string;
};

const Chronicles = () => {
  const [chronicles, setChronicles] = useState<Chronicle[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetch = async () => {
      const response = await request(['chronicles']);

      setChronicles(
        response.items.map((chronicle: Chronicle) => {
          return {
            ...chronicle,
            created_at: DateTime.fromISO(chronicle.created_at, {
              zone: 'utc',
            }).toFormat('dd.MM.yy HH:mm'),
          };
        }),
      );

      setIsLoading(false);
    };

    setIsLoading(true);
    fetch();
  }, []);

  return (
    <Fragment>
      <ul>
        {isLoading && 'Loading ...'}
        {chronicles.map((chronicle) => {
          return (
            <li key={chronicle.id}>
              <p>
                <strong>{chronicle.title}</strong> ({chronicle.created_at})
              </p>
              <p>{chronicle.description}</p>
            </li>
          );
        })}
      </ul>
    </Fragment>
  );
};

export default Chronicles;
