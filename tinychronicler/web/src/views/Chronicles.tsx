import { Fragment } from 'react';
import { DateTime } from 'luxon';
import { Link } from 'react-router-dom';

import Paginator from '~/components/Paginator';

type Chronicle = {
  id: number;
  title: string;
  description: string;
  created_at: string;
};

const Chronicles = () => {
  return (
    <Fragment>
      <h2>Chronicles</h2>
      <Link to="/chronicles/new">Create new Chronicle</Link>
      <Paginator<Chronicle> path={['chronicles']}>
        {({ items, hasPreviousPage, hasNextPage, nextPage, previousPage }) => (
          <ul>
            {items.map((chronicle) => {
              const createdAt = DateTime.fromISO(chronicle.created_at, {
                zone: 'utc',
              })
                .setZone('system')
                .toFormat('dd.MM.yy HH:mm');

              return (
                <li key={chronicle.id}>
                  <p>
                    <strong>{chronicle.title}</strong> ({createdAt})
                  </p>
                  <p>{chronicle.description}</p>
                </li>
              );
            })}
            <button disabled={!hasPreviousPage} onClick={previousPage}>
              &lt;
            </button>
            <button disabled={!hasNextPage} onClick={nextPage}>
              &gt;
            </button>
          </ul>
        )}
      </Paginator>
    </Fragment>
  );
};

export default Chronicles;
