import { useCallback, useEffect, useState } from 'react';

import request from '~/utils/api';

const PAGE_SIZE = 10;

type Props<T> = {
  path: string[];
  children: React.FunctionComponent<{
    items: T[];
    page: number;
    total: number;
    size: number;
    hasNextPage: boolean;
    hasPreviousPage: boolean;
    nextPage: () => void;
    previousPage: () => void;
  }>;
};

const Paginator = <T extends object>({ path, children }: Props<T>) => {
  const [items, setItems] = useState<T[]>([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const response = await request(path, { page, size: PAGE_SIZE });
        setItems(response.items);
        setPage(response.page);
        setTotal(response.total);
      } catch {
        window.alert('Something went wrong');
      }
    };

    fetchAll();
  }, [path, page]);

  const hasNextPage = total > page * PAGE_SIZE;
  const hasPreviousPage = page > 1;

  const nextPage = useCallback(() => {
    if (hasNextPage) {
      setPage((page) => page + 1);
    }
  }, [hasNextPage]);

  const previousPage = useCallback(() => {
    if (hasPreviousPage) {
      setPage((page) => page - 1);
    }
  }, [hasPreviousPage]);

  return children({
    items,
    page,
    size: PAGE_SIZE,
    total,
    hasNextPage,
    hasPreviousPage,
    nextPage,
    previousPage,
  });
};

export default Paginator;
