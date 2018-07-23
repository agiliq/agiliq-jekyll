/**
 * Responds to an HTTP request using data from the request body parsed according
 * to the "content-type" header.
 *
 * @param {Object} req Cloud Function request context.
 * @param {Object} res Cloud Function response context.
 */

var auth = {
    apiKey: 'key-162smw64aaia6-qb-2yngoyr56akjv41',
    domain: 'smtp.mailgun.org'
    }

//var mailgun = require('mailgun-js')(auth)

exports.contactUs = (req, res) => {
  let name;
  let email;
  let data;

  name = req.body.name;
  email = req.body.email;

  data = {
    from: 'hello@agiliq.com',
    subject: 'Welcome!',
    html: `<p>New message from ${name} [${email}]. </p>`,
    'h:Reply-To': 'hello@agiliq.com',
    to: email
  }

//  mailgun.messages().send(data, function (error, body) {
//    console.log(body)
//  })

  res.status(200).send(`${data.html}`);
};
