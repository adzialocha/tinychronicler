import { useCallback, useEffect, useState } from 'react';

import request from '~/utils/api';

const PAGE_SIZE = 10;

type Props<T> = {
  path: string[];
  page: number;
  onChange: (page: number) => void;
  children: React.FunctionComponent<{
    items: T[];
    total: number;
    size: number;
    hasNextPage: boolean;
    hasPreviousPage: boolean;
    nextPage: () => void;
    previousPage: () => void;
  }>;
};

const Paginator = <T extends object>({
  path,
  page = 1,
  onChange,
  children,
}: Props<T>) => {
  const [items, setItems] = useState<T[]>([]);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const response = await request(path, { page, size: PAGE_SIZE });
        setItems(response.items);
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
      onChange(page + 1);
    }
  }, [page, onChange, hasNextPage]);

  const previousPage = useCallback(() => {
    if (hasPreviousPage) {
      onChange(page - 1);
    }
  }, [page, onChange, hasPreviousPage]);

  return children({
    items,
    size: PAGE_SIZE,
    total,
    hasNextPage,
    hasPreviousPage,
    nextPage,
    previousPage,
  });
};

export default Paginator;
