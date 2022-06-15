import React, { useState } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import Divider from "@mui/material/Divider";
import TextField from "@mui/material/TextField";
import List from "@mui/material/List";
import { ListItem } from "@mui/material";
import Button from "@mui/material/Button";

function Home({ submitData }) {
  const [node, setNode] = useState();
  const [energy, setEnergy] = useState();
  const [data, setData] = useState();

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
            onChange={(e) => setNode(e.target.value)}
            style={{ width: "35vw", margin: "20px 0" }}
          />
        </ListItem>
        <ListItem>
          <TextField
            id="filled-basic"
            label="Initial Energy To Each Node"
            variant="filled"
            onChange={(e) => setEnergy(e.target.value)}
            style={{ width: "35vw", margin: "20px 0" }}
          />
        </ListItem>
        <ListItem>
          <TextField
            id="filled-basic"
            label="Data For Each Node"
            variant="filled"
            onChange={(e) => setData(e.target.value)}
            style={{ width: "35vw", margin: "20px 0" }}
          />
        </ListItem>
        <Button variant="contained" onClick={() => submitData({ node, energy, data })}>
          Start
        </Button>
      </div>
      <Box></Box>
    </Container>
  );
}

export default Home;
