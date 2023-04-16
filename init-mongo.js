db.CreateUser({
    user: "admin",
    pwd: "admin",
    roles: [{
      role: "userAdminAnyDatabase",
      db: "admin"
    }]
})