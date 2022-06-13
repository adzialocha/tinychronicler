import { Fragment } from 'react';
import { Formik, Field, Form, ErrorMessage } from 'formik';
import { useNavigate } from 'react-router-dom';
import * as Yup from 'yup';

import request from '~/utils/api';

const ChroniclesNew = () => {
  const navigate = useNavigate();

  return (
    <Fragment>
      <h2>Create new Chronicle</h2>
      <Formik
        initialValues={{ title: '', description: '' }}
        validationSchema={Yup.object({
          title: Yup.string().max(255).required(),
          description: Yup.string().required(),
        })}
        onSubmit={async (values, { setSubmitting }) => {
          try {
            await request(['chronicles'], values, 'POST');
            navigate('/chronicles');
          } catch {
            window.alert('Something went wrong');
          }

          setSubmitting(false);
        }}
      >
        <Form>
          <fieldset>
            <label htmlFor="title">Title</label>
            <Field name="title" id="title" type="text" />
            <ErrorMessage name="title" />
          </fieldset>
          <fieldset>
            <label htmlFor="description">Description</label>
            <Field
              name="description"
              id="description"
              as="textarea"
              type="text"
            />
            <ErrorMessage name="description" />
          </fieldset>
          <button type="submit">Create</button>
        </Form>
      </Formik>
    </Fragment>
  );
};

export default ChroniclesNew;
