import React from "react";

export const UserContext = React.createContext();

export const UserProvider = (props) => {
  const [token, setToken] = React.useState(localStorage.getItem("diseaseFindingToken"));

  React.useEffect(() => {
    const fetchUser = async () => {
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      };

      const response = await fetch(`${process.env.REACT_APP_API_URL}/users`, requestOptions);

      if (!response.ok) {
        setToken(null);
      }
      localStorage.setItem("diseaseFindingToken", token);
    };
    fetchUser();
  }, [token]);

  return (
    <UserContext.Provider value={[token, setToken]}>
      {props.children}
    </UserContext.Provider>
  );
};