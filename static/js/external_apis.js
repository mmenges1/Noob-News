function loadApis(name, speedRun, youtubeurl) {
  var id = "client_id=lafleu2a48dpivopblprona7jhjf3j";
  $.getJSON(
    "https://api.twitch.tv/kraken/videos/top?game=" + name + "&" + id,
    function(obj) {
      for (var i = 0; i < 1; i++) {
        var x = {};
        x.img = obj.videos[i].preview;
        x.content = obj.videos[i].description.substring(0, 20);
        x.url = obj.videos[i].url;
        x.description = obj.videos[i].description;
        x.id = obj.videos[i]._id;
        x.author = obj.videos[i].channel.name;
        x.views = obj.videos[i].views;
        x.title = obj.videos[i].title.substring(0, 20);
        $("#Tdesc").append(x.content);
        $("#Ttitle").append(x.title);
        $("#Tviews").append(x.views);
        $("#Ttitle").append(x.title);
        $("#Turl").append(x.url);
        $("#id").append(x.id);
        $("#streamer").append(x.author);
        iframe =
          "<span><iframe width='560' height='315' src='https://player.twitch.tv/?autoplay=false&video=" +
          x.id +
          "'frameborder='0' allow='accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe></span>";
        $("#frameing").append(iframe);
      }
    },
    "jsonp"
  );
  $.getJSON(
    "https://api.twitch.tv/kraken/videos/" + speedRun + "?" + id,
    function(obj) {
      for (var i = 0; i < 1; i++) {
        var x = {};
        x.author = obj.channel.name;
        x.views = obj.views;
        x.title2 = obj.title.substring(0, 20);
        $("#Stitle").append(x.title2);
        $("#Speedviews").append(x.views);
        $("#Speedstreamer").append(x.author);
      }
    },
    "jsonp"
  );

  $.getJSON(
    " https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=1&playlistId=" +
      youtubeurl +
      "&fields=items/snippet/title,items/snippet/description&key=AIzaSyDu4N6OHRVf81plK5FcmXb1P0L5Ef-nYMY",
    function(data) {
      $.each(data.items, function(i, item) {
        var videoDes = item["snippet"]["description"];
        var title = item["snippet"]["title"];
        $("#desc").append(videoDes);
        $("#title").append(title);
      });
    }
  );
  $.getJSON(
    "https://player.twitch.tv/?autoplay=false&video=" + speedRun,
    function(data) {
      $.each(data.items, function(i, item) {
        console.log(item);
        var videoDes = item["snippet"]["description"];
        var title = item["snippet"]["title"];
        $("#desc").append(videoDes);
        $("#title").append(title);
      });
    }
  );
}
