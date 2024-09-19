import React from 'react';
import remarkGfm from 'remark-gfm';
import Markdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

// ===============================================================================>
// =============================== STYLES ========================================>
// ===============================================================================>

const styles = {
    image: {
        maxWidth: '90%',      
        height: 'auto',          
        borderRadius: '12px',    
        margin: '20px 0',        
        display: 'block',        
        border: '6px inset #2baffc', 
        padding: '12px',         
        backgroundColor: '#fff', 
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', 
    },    
    table: {
        width: '100%',
        borderCollapse: 'collapse' as 'collapse',
    },
    th: {
        border: '1px solid #ddd',
        padding: '8px',
        textAlign: 'left' as 'left',
    },
    td: {
        border: '1px solid #ddd',
        padding: '8px',
        textAlign: 'left' as 'left',
    },
};

// ===============================================================================>
// =============================== FUNCTION ======================================>
// ===============================================================================>

function code(props: any) {
    const { children, className, node, ...rest } = props;
    const match = /language-(\w+)/.exec(className || '');

    if (match) {
        const { ref, key, ...syntaxHighlighterProps } = rest;
        return (
            <SyntaxHighlighter
                language={match[1]}
                style={atomDark}
                PreTag="div"
                children={String(children).replace(/\n$/, '')}
                {...syntaxHighlighterProps}
            />
        );
    } else {
        return (
            <code className={className} {...rest}>
                {children}
            </code>
        );
    }
}

// ===============================================================================>
// =============================== INTERFACE =====================================>
// ===============================================================================>

interface MarkDownProp { children: any };

// ===============================================================================>
// ================================== JSX ========================================>
// ===============================================================================>

const MarkDown: React.FC<MarkDownProp> = ({ children }) => {
    return (
        <Markdown
            components={{
                code,
                img: ({ node, ...props }) => <img style={styles.image} {...props} />,
                table: ({ node, ...props }) => <table style={styles.table} {...props} />,
                th: ({ node, ...props }) => <th style={styles.th} {...props} />,
                td: ({ node, ...props }) => <td style={styles.td} {...props} />,
            }}
            remarkPlugins={[remarkGfm]}
        >
            {children}
        </Markdown>
    );
};
export default MarkDown;
