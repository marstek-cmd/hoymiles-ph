/**
 * Hoymiles PH — quote / contact form receiver
 *
 * Every form sent on the website becomes one new row in this Google Sheet,
 * and an email alert goes to NOTIFY_EMAIL (this address is never shown on the website).
 *
 * Setup: see "Connect the quote form" in README.md.
 */

// Who gets an email when a new request comes in (comma-separate several addresses).
var NOTIFY_EMAIL = 'you@example.com';

var HEADERS = ['Received', 'Type', 'Name', 'Phone', 'Email', 'City', 'Address',
               'Products', 'Current solar', 'Message', 'Sent from page'];

function doPost(e) {
  var p = (e && e.parameter) || {};

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Requests');
  if (!sheet) sheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet('Requests');
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
  }

  var row = [new Date(), p.topic || 'Quote', p.name, p.phone, p.email, p.city, p.address,
             p.products, p.solar, p.notes, p.page].map(function (v) {
    v = v === undefined ? '' : v;
    // stop spreadsheet formulas being injected through the form
    return (typeof v === 'string' && /^[=+\-@]/.test(v)) ? "'" + v : v;
  });
  sheet.appendRow(row);

  if (NOTIFY_EMAIL && NOTIFY_EMAIL.indexOf('example.com') === -1) {
    var lines = HEADERS.map(function (h, i) { return h + ': ' + (row[i] || '—'); }).join('\n');
    MailApp.sendEmail({
      to: NOTIFY_EMAIL,
      subject: 'New ' + (p.topic || 'Quote') + ' request — ' + (p.name || '') + ', ' + (p.city || ''),
      body: lines + '\n\nAll requests: ' + SpreadsheetApp.getActiveSpreadsheet().getUrl()
    });
  }

  return ContentService.createTextOutput('ok');
}

// Lets you check the web-app link in a browser: it should say "Hoymiles PH form is running".
function doGet() {
  return ContentService.createTextOutput('Hoymiles PH form is running');
}
