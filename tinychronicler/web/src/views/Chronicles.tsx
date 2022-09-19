import { Fragment } from 'react';
import {
  Table,
  TableBody,
  TableDataCell,
  TableHead,
  TableHeadCell,
  TableRow,
  Toolbar,
  Window,
  WindowContent,
  WindowHeader,
} from 'react95';

import type { Chronicle } from '~/types';

import Link from '~/components/Link';
import Paginator from '~/components/Paginator';
import { formatDate } from '~/utils/format';

const Chronicles = () => {
  return (
    <Fragment>
      <Window style={{ width: '100%', maxWidth: 1000 }}>
        <WindowHeader>Chronicles</WindowHeader>
        <Toolbar>
          <Link to="/chronicles/new" variant="menu" size="sm">
            Create new
          </Link>
        </Toolbar>
        <WindowContent>
          <Paginator<Chronicle> path={['chronicles']}>
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
                          <TableDataCell>{chronicle.description}</TableDataCell>
                          <TableDataCell>
                            <Link
                              to={`/chronicles/${chronicle.id}/edit`}
                              variant="flat"
                              size="sm"
                            >
                              Edit
                            </Link>
                          </TableDataCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
                <div style={{ paddingTop: 7 }}>
                  <Link disabled={!hasPreviousPage} onClick={previousPage}>
                    &lt;
                  </Link>
                  <Link disabled={!hasNextPage} onClick={nextPage}>
                    &gt;
                  </Link>
                </div>
              </>
            )}
          </Paginator>
        </WindowContent>
      </Window>
    </Fragment>
  );
};

export default Chronicles;
