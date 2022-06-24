
const URL = "https://raw.githubusercontent.com/kawadasatoshi/twitter_network/main/{{ screen_name }}"
const SCREEN_NAME = "{{ screen_name }}"
console.log("LOG: start main.js")

$.getJSON(URL, (data) => {
    console.log("LOG:", data)

    var members_data = data.nodes.map(function(row){
        return {
            "title": (row.name).replace("@",""),
            "img": row.img
        }
    }).slice(0,8)
    console.log("LOG:", members_data)
    const membersView = new MembersView(members_data)
    membersView.apply()

})


