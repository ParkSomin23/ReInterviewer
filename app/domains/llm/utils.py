import re
import json

from pydantic import BaseModel


def get_system_prompt(prompt_template, clean_schema_format):

    system_content = prompt_template.replace(
        "__SCHEMA_PLACEHOLDER__", clean_schema_format
    )

    system_msg = {"role": "system", "content": system_content}

    return system_msg


def clean_schema_format(cls: type[BaseModel]) -> str:

    raw_schema = cls.model_json_schema()
    root_field_name = list(raw_schema.get("properties", {}).keys())[0]

    if "$defs" in raw_schema:
        sub_model_name = list(raw_schema["$defs"].keys())[0]
        item_properties = raw_schema["$defs"][sub_model_name]["properties"]
    else:
        item_properties = raw_schema.get("properties", {})

    simplified_fields = {}
    for field_name, info in item_properties.items():
        if "anyOf" in info:
            types = [t["type"] for t in info["anyOf"]]
            simplified_fields[field_name] = " or ".join(types)
        else:
            simplified_fields[field_name] = info.get("type", "string")

    is_array = (
        raw_schema.get("properties", {}).get(root_field_name, {}).get("type") == "array"
    )

    clean_structure = {
        root_field_name: [simplified_fields] if is_array else simplified_fields
    }

    return json.dumps(clean_structure, indent=2, ensure_ascii=False), clean_structure


def parse_interview_response(ollama_response, schema_dict: dict):

    try:
        # Content 추출
        if hasattr(ollama_response, "message") and hasattr(
            ollama_response.message, "content"
        ):
            raw_text = ollama_response.message.content
        elif isinstance(ollama_response, dict):
            raw_text = ollama_response["message"]["content"]
        else:
            raw_text = str(ollama_response)

        # JSON 추출
        json_match = re.search(
            r"```json\s*(.*?)\s*```", raw_text, re.DOTALL | re.IGNORECASE
        )

        if json_match:
            clean_json_str = json_match.group(1).strip()
        else:
            json_fallback = re.search(r"(\{.*\})", raw_text, re.DOTALL)
            clean_json_str = (
                json_fallback.group(1).strip() if json_fallback else raw_text
            )

        data = json.loads(clean_json_str)

        # 기존 schema에 값 넣기
        root_key = list(schema_dict.keys())[0]
        is_array = isinstance(schema_dict[root_key], list)

        if is_array:
            schema_fields_info = schema_dict[root_key][0]
        else:
            schema_fields_info = schema_dict[root_key]

        schema_keys = list(schema_fields_info.keys())

        target_payload = data.get(root_key)
        if target_payload is not None:
            items_to_clean = (
                target_payload
                if is_array and isinstance(target_payload, list)
                else [target_payload]
            )

            for item in items_to_clean:
                if not isinstance(item, dict):
                    continue

                for key in schema_keys:
                    val = item.get(key)

                    expected_type = schema_fields_info.get(key, "")

                    if val == "None":
                        item[key] = None

                    elif val is None:
                        item[key] = None

                    elif val is False and "string" in expected_type:
                        item[key] = None

        return json.dumps(data, ensure_ascii=False)

    except Exception as e:
        raise ValueError(
            f"스키마 구조가 맞지 않습니다.\n"
            f"실제 에러: {e}\n"
            f"최종 처리하려던 JSON 문자열: {locals().get('clean_json_str', '추출 실패')}"
        ) from e
