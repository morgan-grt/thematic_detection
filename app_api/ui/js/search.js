let hostname = "/graphql/?query=";
let mongodbSize;

function spacyLabel(label)
{
    return label.replace(/ /g, '-');
}

function getMongodbSize()
{
    let query = `{CountItem}`;

    d3.json(`${hostname}${query}`)
            .then(updateMongodbSize);
}

function updateMongodbSize(root)
{
    mongodbSize = root.data.CountItem;
    console.log(mongodbSize);
}

function getMogonLabels()
{
    let query = `{Distinct}`
}

getMongodbSize();

function query()
{
    let query = `{
        Mails`
        + `{id, subject}}`;

    d3.json(`${hostname}${query}`)
            .then(getQuery);
}

function getQuery(root)
{
	console.log(root.data.Mails);
}



function getFrequentLabel()
{
    let query = `{
        CountDistinct {
            name
            count
        }}`;

    d3.json(`${hostname}${query}`)
            .then(showLabels);
}

function showLabels(root)
{
    for (index in root.data.CountDistinct)
    {
        let label = root.data.CountDistinct[index].name;
        d3.select('#labels-div')
            .append('div')
                .attr('class', 'div-label')
                .attr('id', spacyLabel(label))
                .text(`${root.data.CountDistinct[index].name}`)
                .on("click", updateListLabel);
    }
}

let updateListLabel = function(e, i) 
{
    let label = e.target.innerText;
    if (labelChoosed.indexOf(label) === -1)
    {
        labelChoosed.push(label);
        $(`#${spacyLabel(label)}`).addClass('choosed');
    }
    else
    {
        labelChoosed = labelChoosed.filter(item => item !== label);
        $(`#${spacyLabel(label)}`).removeClass('choosed');
    }
    $('#mails-div').empty();
    getMailByLabel();
}

let labelChoosed = [];
getFrequentLabel();

function arrayToString(arr)
{
    result = '['
    for (let i = 0; i < arr.length; i++)
    {
        result += `"${arr[i]}"`
        if (i < arr.length - 1)
            result += ','
    }
    result += ']'
    return result;
}

function getMailByLabel()
{
    let query = `{
        MailByAllLabel (labelChoosed: ${arrayToString(labelChoosed)}) {
            _id
            body
            subject
            date
            fromName
            fromMail
            language
            isCFP
            labels {
              name
              count
            }
        }}`;

    d3.json(`${hostname}${query}`)
            .then(showMails);
}

function showMails(root)
{
    for (let index in root.data.MailByAllLabel) {
        let id = root.data.MailByAllLabel[index]._id;
        let mail_div = d3.select('#mails-div')
            .append('div')
            .attr('class', 'div-mail reduced')
            .attr('id', spacyLabel(id))
            .on("click", updateListMail);
        mail_div.append('p')
            .attr('class', 'mail-author')
            .text(`Author: ${root.data.MailByAllLabel[index].fromName}`);
        mail_div.append('p')
            .attr('class', 'mail-email')
            .text(`Mail: ${root.data.MailByAllLabel[index].fromMail}`);
        mail_div.append('p')
            .attr('class', 'mail-date')
            .text(`Date: ${root.data.MailByAllLabel[index].date}`);
        mail_div.append('p')
            .attr('class', 'mail-body')
            .text(`Body: ${root.data.MailByAllLabel[index].body}`)
            .on("click", function(e) {
                if ($(`#${id}`).hasClass('reduced'))
                    $(`#${id}`).removeClass('reduced');
                else
                    $(`#${id}`).addClass('reduced');
            });
            
    }
}

let updateListMail = function(e){}