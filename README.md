#### Backend

Runs in chalice and uses AWS client boto3.

Install python

pip install pipenv

pipenv install boto3

pipenv install botocore

pipenv install chalice

pipenv shell

cd backend

chalice local

This will start the backend running on 127.0.0.1:8000

CTRL+C will halt the server.


#### Frontend

Install NodeJS. (Built in NodeJS 19.9.x)

npm install react-router react-router-dom @mui/material @emotion/react @emotion/styled @mui/icons-material @fontsource/roboto formik yup axios

cd frontend

npm start

This will start the frontend running on 127.0.0.1:5000

CTRL+C will halt the server


References
NodeJS Material UI:
https://mui.com/material-ui/getting-started/installation/
Useage: has material UI design and also Alert box handling!

Formik:
https://formik.org/docs/tutorial   and  https://formik.org/docs/guides/validation
Useage: easier form handling in React

Yup:
https://github.com/jquense/yup
On advice and examples of Formik, this is good for form validation

Axios:
https://axios-http.com/
Does the HTTP operations akin to curl
