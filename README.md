# Hack the Planet 2021

This repo contains the API for the [Hack the Planet Contest](https://dev.to/devteam/announcing-the-new-relic-hack-the-planet-contest-on-dev-5d)

## What I built

An API and data sender to consume raw data from a CSV downloaded from the European Environment Agency. More specifically, from the Marine LitterWatch project.

### Category Submission: 

Science and Observation

### App Link

https://hacktheplanet.mywire.org/

### Screenshots

![Screen Shot 2021-02-18 at 15.27.51](https://www.therelicans.com/remoteimages/uploads/articles/dcv9km7tr6f8ya44btbi.png)

![Screen Shot 2021-02-18 at 15.28.08](https://www.therelicans.com/remoteimages/uploads/articles/csf9tkzfzcs6dpohfz6t.png)

![Screen Shot 2021-02-21 at 21.10.57](https://www.therelicans.com/remoteimages/uploads/articles/18v5sb4s4k8fia6plr4o.png) 

![Screen Shot 2021-02-18 at 15.28.30](https://www.therelicans.com/remoteimages/uploads/articles/sazxwhz8n5mgmbywdgon.png)

![Screen Shot 2021-02-28 at 00.32.44](https://www.therelicans.com/remoteimages/uploads/articles/bgmuoccn3nmljs2v88jv.png)

![Screen Shot 2021-02-21 at 21.07.54](https://www.therelicans.com/remoteimages/uploads/articles/w0s9pzdmza8j4xc79nct.png)

![Screen Shot 2021-02-21 at 21.08.32](https://www.therelicans.com/remoteimages/uploads/articles/bqstxrcdyozqnmsful0o.png)

![Screen Shot 2021-02-28 at 20.15.33](https://www.therelicans.com/remoteimages/uploads/articles/e1ijtzagp8nipvr1ib2i.png) 

### Description

Python Flask solution that prepares the data and serves it through an API in JSON Format. The database is updated automatically from the EEA and the data sent every minute to *New Relic*. All the solution has been created in a K8S Cluster. The Infrastructure architecture and the manifests are also part of the code.

### Link to Source Code

https://github.com/imjoseangel/hacktheplanet2021

### Permissive License

MIT

## Background

Litter, plastics in particular, is accumulating in our seas and coasts. Information and data on marine litter is essential for tackling it.

Marine LitterWatch (MLW) is a European Environment Agency (EEA) participatory science approach that empowers individuals and communities to take up action and fill in the data gaps that hamper the implementation of essential measures towards litter-free coasts and seas. The EEA MLW community members have collected more than 2 million beach litter items with 3288 beach surveys and registered them to MLW database in the last 7 years. More than 80 % of these items are plastics.

This *API Solution* is an approach to help consuming the data from the MLW project.

### How I built it
 
I have used the following items:

* The **Event API** as the main resource to send the data every 10 minutes.
* The **query builder** and **data explorer** to create the graphs.
* The graphs **Share/Get Chart Link** (Embeddables) option to embed them into the portal.
* The **Dashboard** to keep the graphs.
* The **APM** to monitor the application.
* **Notification Policies** to receive unavailability Alerts.
* **Synthetic Monitor** to check availability in different parts of the world.
