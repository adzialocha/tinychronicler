import { Fragment } from 'react';
import { useFormik } from 'formik';
import { useNavigate } from 'react-router-dom';
import * as Yup from 'yup';
import styled from 'styled-components';
import {
  Button,
  Radio,
  TextField,
  Fieldset,
  Window,
  WindowContent,
  WindowHeader,
} from 'react95';

import request from '~/utils/api';

const LANGUAGES = {
  Chinese: 'cn',
  German: 'de',
  English: 'en',
  Spanish: 'es',
  French: 'fr',
  Italian: 'it',
  Japanese: 'jp',
  Polish: 'pl',
  Russian: 'ru',
};

const DEFAULT_LANGUAGE = 'en';

type LanguagesKey = keyof typeof LANGUAGES;

const RadioButtonList = styled.div`
  display: flex;
  flex-direction: column;
`;

const ChroniclesNew = () => {
  const navigate = useNavigate();
  const formik = useFormik({
    initialValues: { title: '', description: '', language: DEFAULT_LANGUAGE },
    validationSchema: Yup.object({
      title: Yup.string().max(255).required(),
      description: Yup.string().required(),
      language: Yup.string().length(2).required(),
    }),
    onSubmit: async (values, { setSubmitting }) => {
      try {
        await request(['chronicles'], values, 'POST');
        navigate('/chronicles');
      } catch {
        window.alert('Something went wrong');
      }

      setSubmitting(false);
    },
  });

  return (
    <Fragment>
      <Window style={{ width: '100%', maxWidth: 600 }}>
        <WindowHeader>Create new Chronicle</WindowHeader>
        <WindowContent>
          <form onSubmit={formik.handleSubmit}>
            <Fieldset label="Information">
              <fieldset>
                <label htmlFor="title">Title</label>
                <TextField
                  id="title"
                  name="title"
                  value={formik.values.title}
                  onChange={formik.handleChange}
                  fullWidth
                />
                {formik.touched.title && Boolean(formik.errors.title) && (
                  <p>
                    <em>{formik.errors.title}</em>
                  </p>
                )}
              </fieldset>
              <fieldset>
                <label htmlFor="description">Description</label>
                <TextField
                  id="description"
                  name="description"
                  multiline
                  rows={4}
                  value={formik.values.description}
                  onChange={formik.handleChange}
                  fullWidth
                />
                {formik.touched.description &&
                  Boolean(formik.errors.description) && (
                    <p>
                      <em>{formik.errors.description}</em>
                    </p>
                  )}
              </fieldset>
            </Fieldset>
            <br />
            <Fieldset label="Language">
              <fieldset>
                <RadioButtonList>
                  {Object.keys(LANGUAGES).map((name) => {
                    const value = LANGUAGES[name as LanguagesKey];

                    return (
                      <label key={name} htmlFor={name}>
                        <Radio
                          id={name}
                          name="language"
                          value={value}
                          checked={formik.values.language === value}
                          onChange={formik.handleChange}
                        />
                        {name}
                      </label>
                    );
                  })}
                </RadioButtonList>
                {formik.touched.language && Boolean(formik.errors.language) && (
                  <p>
                    <em>{formik.errors.language}</em>
                  </p>
                )}
              </fieldset>
            </Fieldset>
            <div style={{ paddingTop: 7 }}>
              <Button type="submit">Create</Button>
            </div>
          </form>
        </WindowContent>
      </Window>
    </Fragment>
  );
};

export default ChroniclesNew;
