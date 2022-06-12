import { Fragment, useCallback, useEffect, useState } from 'react';
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
  const [values, setValues] = useState({
    title: '',
    description: '',
  });

  const fetchAll = async () => {
    const response = await request(['chronicles']);

    setChronicles(
      response.items.map((chronicle: Chronicle) => {
        return {
          ...chronicle,
          created_at: DateTime.fromISO(chronicle.created_at, {
            zone: 'utc',
          })
            .setZone('system')
            .toFormat('dd.MM.yy HH:mm'),
        };
      }),
    );
  };

  const create = useCallback(async () => {
    try {
      await request(['chronicles'], values, 'POST');

      setValues({
        title: '',
        description: '',
      });

      await fetchAll();
    } catch {
      window.alert('Something went wrong ..');
    }
  }, [values]);

  useEffect(() => {
    fetchAll();
  }, []);

  const change = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;

    setValues((values) => {
      return {
        ...values,
        [name]: value,
      };
    });
  }, []);

  const submit = useCallback(
    async (event: React.FormEvent) => {
      event.preventDefault();
      create();
    },
    [create],
  );

  return (
    <Fragment>
      <h2>Chronicles</h2>
      <ul>
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
      <h2>Create new Chronicle</h2>
      <form onSubmit={submit}>
        <fieldset>
          <label htmlFor="title">Title</label>
          <input
            name="title"
            id="title"
            value={values.title}
            type="text"
            onChange={change}
          />
        </fieldset>
        <fieldset>
          <label htmlFor="description">Description</label>
          <input
            name="description"
            id="description"
            type="text"
            value={values.description}
            onChange={change}
          />
        </fieldset>
        <input type="submit" value="Create" />
      </form>
    </Fragment>
  );
};

export default Chronicles;
