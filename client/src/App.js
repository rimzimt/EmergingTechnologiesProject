import React, { useState } from 'react';
import AppBar from '@material-ui/core/AppBar';
import { makeStyles } from '@material-ui/core/styles';
import Toolbar from '@material-ui/core/Toolbar'
import TypoGraphy from '@material-ui/core/Typography'
import TextareaAutosize from '@material-ui/core/TextareaAutosize';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    height: "100%",
    width: "100%",
    padding: 30,
    margin: 5,
  },
  control: {
    padding: theme.spacing(2),
  },
  textArea: {
    width: "100%"
  },
  middle: {
    maxWidth: "fit-content"
  },
  inner: {
    flexDirection: "column"
  },
  dropDown: {
    marginBottom: 20,
  }
}));



export default function App() {
  const classes = useStyles();
  const [content, setContent] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [compression, setCompression] = useState("0.2");
  const [open, setOpen] = React.useState(false);

  const handleChange = (event) => {
    setCompression(event.target.value);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleOpen = () => {
    setOpen(true);
  };

  const fetchSummary = () => {
    setLoading(true);
    fetch('/articles', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "course": "demo",
        content,
        name: "temp"
      })
    }
    ).then(response => response.json())
      .then(data => {
        fetch(`/articles/${data.id}/summaries`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            ratio: compression,
            name: "temp"
          })
        }
        ).then(response => response.json())
          .then(data => {
            setLoading(false);
            setSummary(data.content);
          })
          .catch((error) => {
            setLoading(false);
            console.error('Error:', error);
          });
      })
      .catch((error) => {
        setLoading(false);
        console.error('Error:', error);
      });
  }
  return (
    <div className="App">
      <AppBar color="primary" position="static">
        <Toolbar>
          <TypoGraphy variant="h4"
            color="inherit"
          >
            BERT Content Summarizer
           </TypoGraphy>
        </Toolbar>
      </AppBar>
      <Grid container
        className={classes.root}
        spacing={2}
        alignItems="center"
        justify="center">
        <Grid key="left" xs={5} item>
          <TextareaAutosize value={content} onChange={(e) => {
            setContent(e.target.value)
          }} className={classes.textArea} aria-label="left textarea" rowsMin={40} placeholder="Paste your content here" />
        </Grid>
        <Grid key="middle" xs={2} className={classes.middle} item>
          <Grid key="inner" className={classes.inner} justify="center" container>
          <FormControl className={classes.formControl}>
            <InputLabel id="demo-simple-select-label">Compression</InputLabel>
            <Select
              labelId="demo-controlled-open-select-label"
              id="demo-controlled-open-select"
              open={open}
              onClose={handleClose}
              onOpen={handleOpen}
              value={compression}
              onChange={handleChange}
              className={classes.dropDown}
            >
              <MenuItem value={0.1}>0.1</MenuItem>
              <MenuItem value={0.2}>0.2</MenuItem>
              <MenuItem value={0.3}>0.3</MenuItem>
            </Select>
          </FormControl>
          <Button variant="contained" color="primary" disabled={loading} onClick={fetchSummary}>
            {loading ? "Generating..." : "> Summarize >"}
          </Button>
          </Grid>
        </Grid>
        <Grid key="right" xs={5} item>
          <TextareaAutosize value={summary} onChange={(e) => {
            setSummary(e.target.value)
          }} className={classes.textArea} aria-label="right textarea" rowsMin={40} placeholder="Summary will be generated here" />
        </Grid>
      </Grid>
    </div>
  );
}
