﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InputColliderClass : MonoBehaviour {

    public int m_value;
    public GO m_go;
    public SpriteRenderer m_goSpriteRenderer;

	// Use this for initialization
	void Start () {
        m_value = 0;
        m_go = new GO(gameObject);
        m_goSpriteRenderer = m_go.getGO().GetComponent<SpriteRenderer>();
        m_goSpriteRenderer.color = Color.green;
    }

    // Update is called once per frame
    void Update () {

    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.gameObject.CompareTag("Platform"))
        {
            m_value = 1;
            if (m_goSpriteRenderer != null)
            {
                m_goSpriteRenderer.color = Color.blue;
            }
        }
        else if (other.gameObject.CompareTag("Tracker"))
        {
            m_value = -1;
            if (m_goSpriteRenderer != null)
            {
                m_goSpriteRenderer.color = Color.red;
            }
        }
    }

    private void OnTriggerStay2D(Collider2D other)
    {
        if (other.gameObject.CompareTag("Platform"))
        {
            m_value = 1;
            if (m_goSpriteRenderer != null)
            {
                m_goSpriteRenderer.color = Color.blue;
            }
        }
        else if (other.gameObject.CompareTag("Tracker"))
        {
            m_value = -1;
            if (m_goSpriteRenderer != null)
            {
                m_goSpriteRenderer.color = Color.red;
            }
        }
    }

    private void OnTriggerExit2D(Collider2D other)
    {
        if (other.gameObject.CompareTag("Platform"))
        {
            m_value = 0;
            if (m_goSpriteRenderer != null)
            {
                m_goSpriteRenderer.color = Color.green;
            }
        }
        else if (other.gameObject.CompareTag("Tracker"))
        {
            m_value = 0;
            if (m_goSpriteRenderer != null)
            {
                m_goSpriteRenderer.color = Color.green;
            }
        }
    }
}