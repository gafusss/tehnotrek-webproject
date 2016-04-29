function rateAjax(url, content_type_id, pk) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                var response = JSON.parse(xhr.responseText);
                var ratingspan = document.getElementById("span-rating-" +
                    content_type_id.toString() +
                    "-" +
                    pk.toString());
                ratingspan.innerText = response.rating;
                if (response.rating == 0) {
                    ratingspan.className = "span-rating-zero";
                } else if (response.rating < 0) {
                    ratingspan.className = "span-rating-negative";
                } else {
                    ratingspan.className = "span-rating-positive";
                }
                var value = response.like;
                var likesubmit = document.getElementById("input-submit-like-" +
                    content_type_id.toString() +
                    "-" +
                    pk.toString() +
                    "-True");
                var dislikesubmit = document.getElementById("input-submit-like-" +
                    content_type_id.toString() +
                    "-" +
                    pk.toString() +
                    "-False");
                if (value == true) {
                    likesubmit.disabled = true;
                    likesubmit.className = "input-submit-like-disabled";
                    dislikesubmit.disabled = false;
                    dislikesubmit.className = "input-submit-like-False";
                } else {
                    likesubmit.disabled = false;
                    likesubmit.className = "input-submit-like-True";
                    dislikesubmit.disabled = true;
                    dislikesubmit.className = "input-submit-like-disabled";
                }
                //document.getElementById("td-exploit-rating").innerHTML = xhr.responseText;
            }
        }
    };
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    xhr.setRequestHeader("X-Requested-With", 'XMLHttpRequest');
    xhr.send();
}

