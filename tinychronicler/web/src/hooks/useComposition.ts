import { useEffect, useState } from 'react';

import type { Composition } from '~/types';

import request from '~/utils/api';

export default function useComposition(
  chronicleId?: number | string,
  id?: number | string,
) {
  const [loading, setLoading] = useState(true);

  const [composition, setComposition] = useState<Composition>({
    created_at: '',
    data: undefined,
    id: 0,
    is_ready: false,
    title: '',
    version: 0,
  });

  useEffect(() => {
    const load = async () => {
      if (!id || !chronicleId) {
        return;
      }

      setLoading(true);

      const response = await request([
        'chronicles',
        chronicleId.toString(),
        'compositions',
        id.toString(),
      ]);
      setComposition(response);

      setLoading(false);
    };

    load();
  }, [chronicleId, id]);

  return { loading, composition };
}
