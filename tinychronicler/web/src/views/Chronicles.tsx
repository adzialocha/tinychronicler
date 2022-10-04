import { Fragment, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Hourglass,
  Table,
  TableBody,
  TableDataCell,
  TableHead,
  TableHeadCell,
  TableRow,
  Window,
  WindowContent,
  WindowHeader,
} from 'react95';

import type { Chronicle } from '~/types';

import Link from '~/components/Link';
import Paginator from '~/components/Paginator';
import request from '~/utils/api';
import { formatDate } from '~/utils/format';

const Chronicles = () => {
  const [search, setSearch] = useSearchParams();
  const [loading, setLoading] = useState(false);
  const page = search.get('page');

  const onDelete = async (id: number) => {
    const answer = window.confirm('Are you sure?');

    if (answer) {
      setLoading(true);

      try {
        await request(['chronicles', id.toString()], undefined, 'DELETE');
      } catch (error) {
        window.alert(error);
      }

      setLoading(false);
    }
  };

  return (
    <Fragment>
      <Window style={{ width: '100%', maxWidth: 1000 }}>
        <WindowHeader>Chronicles</WindowHeader>
        <WindowContent>
          {loading ? (
            <Hourglass />
          ) : (
            <Paginator<Chronicle>
              page={page ? parseInt(page, 10) : 1}
              onChange={(page) => {
                setSearch({ page: page.toString() });
              }}
              path={['chronicles']}
            >
              {({
                items,
                hasPreviousPage,
                hasNextPage,
                nextPage,
                previousPage,
              }) => (
                <>
                  <Table>
                    <TableHead>
                      <TableRow head>
                        <TableHeadCell>ID</TableHeadCell>
                        <TableHeadCell>Title</TableHeadCell>
                        <TableHeadCell>Created</TableHeadCell>
                        <TableHeadCell>Description</TableHeadCell>
                        <TableHeadCell>Actions</TableHeadCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {items.map((chronicle) => {
                        return (
                          <TableRow key={chronicle.id}>
                            <TableDataCell>{chronicle.id}</TableDataCell>
                            <TableDataCell>{chronicle.title}</TableDataCell>
                            <TableDataCell>
                              {formatDate(chronicle.created_at)}
                            </TableDataCell>
                            <TableDataCell>
                              {chronicle.description.slice(0, 75)}
                            </TableDataCell>
                            <TableDataCell>
                              <Link
                                to={`/chronicles/${chronicle.id}/edit`}
                                variant="flat"
                                size="sm"
                              >
                                Edit
                              </Link>
                              &nbsp;
                              <Link
                                onClick={() => onDelete(chronicle.id)}
                                variant="flat"
                                size="sm"
                              >
                                Delete
                              </Link>
                            </TableDataCell>
                          </TableRow>
                        );
                      })}
                    </TableBody>
                  </Table>
                  <div
                    style={{
                      display: 'flex',
                      paddingTop: 7,
                      justifyContent: 'space-between',
                    }}
                  >
                    <div>
                      <Link disabled={!hasPreviousPage} onClick={previousPage}>
                        &lt;
                      </Link>
                      <Link disabled={!hasNextPage} onClick={nextPage}>
                        &gt;
                      </Link>
                    </div>
                    <Link to="/chronicles/new">Create new chronicle</Link>
                  </div>
                </>
              )}
            </Paginator>
          )}
        </WindowContent>
      </Window>
    </Fragment>
  );
};

export default Chronicles;
