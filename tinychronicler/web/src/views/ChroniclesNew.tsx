import { Fragment } from 'react';
import { useFormik } from 'formik';
import { useNavigate } from 'react-router-dom';
import * as Yup from 'yup';
import {
  Button,
  TextField,
  Window,
  WindowContent,
  WindowHeader,
} from 'react95';

import request from '~/utils/api';

const ChroniclesNew = () => {
  const navigate = useNavigate();
  const formik = useFormik({
    initialValues: { title: '', description: '' },
    validationSchema: Yup.object({
      title: Yup.string().max(255).required(),
      description: Yup.string().required(),
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
