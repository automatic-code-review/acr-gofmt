import subprocess

import automatic_code_review_commons as commons


def review(config):
    message = config['message']
    path_source = config['path_source']
    changes = config['merge']['changes']

    comments = []

    for change in changes:
        if change['deleted_file']:
            continue

        new_path = change['new_path']
        path = path_source + "/" + new_path

        if path.endswith(".go"):
            result = subprocess.run(["gofmt", "-d", path], capture_output=True, text=True)

            if result.stdout:
                comment = commons.comment_create(
                    comment_id=commons.comment_generate_id(new_path),
                    comment_path=new_path,
                    comment_description=message.replace("${FILE_PATH}", new_path),
                    comment_snipset=False,
                    comment_end_line=1,
                    comment_start_line=1,
                )
                comments.append(comment)

    return comments
