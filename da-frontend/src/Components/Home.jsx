import React, { useState } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import Divider from "@mui/material/Divider";
import TextField from "@mui/material/TextField";
import List from "@mui/material/List";
import { ListItem } from "@mui/material";
import Button from "@mui/material/Button";
import { lightGreen } from "@mui/material/colors";

const getTemp = () => {
  return 27 + Math.floor(Math.random() * 10 + 1);
};

function Home({ submitData }) {
  const [node, setNode] = useState();
  const [energy, setEnergy] = useState();
  const [data, setData] = useState();

  const genRandTemp = (n) => {
    let tempData = [];
    for (let i = 0; i < n; i++) {
      tempData.push(getTemp());
    }
    console.log(tempData);
    return tempData;
  };

  const SettNode = (v) => {
    setNode(v);
    setData(genRandTemp(v));
  };

  return (
    <Container
      sx={{
        padding: "20px",
        width: "100%",
        maxWidth: 500,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Typography variant="h3" gutterBottom component="div">
        Welcome
      </Typography>
      <Divider />
      <div>
        <ListItem>
          <TextField
            id="filled-basic"
            label="Number Of Sensor Nodes"
            variant="filled"
            color="success"
            onChange={(e) => SettNode(e.target.value)}
            style={{ width: "35vw", margin: "20px 0" }}
          />
        </ListItem>
      </div>
      <p>
        {data
          ? data.map((d, i) => (
              <span key={i} style={{ padding: "5px", margin: "5px" }}>
                {i + 1} : {d},
              </span>
            ))
          : "Enter Number of nodes"}
      </p>
      <div>
        <ListItem>
          <TextField
            id="filled-basic"
            label="Initial Energy To Each Node"
            variant="filled"
            onChange={(e) => setEnergy(e.target.value)}
            style={{ width: "35vw", margin: "20px 0" }}
          />
        </ListItem>
      </div>
      {/* <ListItem>
          <TextField
            id="filled-basic"
            label="Data For Each Node"
            variant="filled"
            onChange={(e) => setData(e.target.value)}
            style={{ width: "35vw", margin: "20px 0" }}
          />
        </ListItem> */}

      <Button variant="contained" onClick={() => submitData({ node, energy, data })}>
        Start
      </Button>
    </Container>
  );
}

export default Home;
